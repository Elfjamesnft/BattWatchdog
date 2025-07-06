import pandas as pd
from datetime import datetime

class BatteryAbuseDetector:
    def __init__(self):
        self.abuse_thresholds = {
            'overcharge': 100,       # SOC > 100%
            'deep_discharge': 20,    # SOC < 20%
            'voltage_spike': 0.5,    # Voltage change > 0.5V in 1 reading
            'current_surge': 2.0     # Current change > 2A in 1 reading
        }
        self.abuse_log = []

    def analyze_log(self, log_path='data/battery_log.csv'):
        """Analyze battery log for abusive patterns"""
        try:
            df = pd.read_csv(log_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            for i in range(1, len(df)):
                self._check_overcharge(df.iloc[i])
                self._check_deep_discharge(df.iloc[i])
                self._check_voltage_spike(df.iloc[i-1], df.iloc[i])
                self._check_current_surge(df.iloc[i-1], df.iloc[i])
                
            return self.abuse_log
            
        except Exception as e:
            return [f"Error analyzing log: {str(e)}"]

    def _check_overcharge(self, current):
        if current['soc'] > self.abuse_thresholds['overcharge']:
            self.abuse_log.append({
                'timestamp': current['timestamp'],
                'type': 'Overcharge',
                'value': current['soc'],
                'message': f"Dangerous overcharge: {current['soc']}% SOC"
            })

    def _check_deep_discharge(self, current):
        if current['soc'] < self.abuse_thresholds['deep_discharge']:
            self.abuse_log.append({
                'timestamp': current['timestamp'],
                'type': 'Deep Discharge',
                'value': current['soc'],
                'message': f"Deep discharge: {current['soc']}% SOC"
            })

    def _check_voltage_spike(self, previous, current):
        delta = abs(current['voltage'] - previous['voltage'])
        if delta > self.abuse_thresholds['voltage_spike']:
            self.abuse_log.append({
                'timestamp': current['timestamp'],
                'type': 'Voltage Spike',
                'value': delta,
                'message': f"Sudden voltage change: {delta:.2f}V"
            })

    def _check_current_surge(self, previous, current):
        if 'current' in current and 'current' in previous:
            delta = abs(current['current'] - previous['current'])
            if delta > self.abuse_thresholds['current_surge']:
                self.abuse_log.append({
                    'timestamp': current['timestamp'],
                    'type': 'Current Surge',
                    'value': delta,
                    'message': f"Sudden current change: {delta:.2f}A"
                })

def generate_abuse_report(log_path='data/battery_log.csv'):
    """Generate a formatted abuse report"""
    detector = BatteryAbuseDetector()
    abuses = detector.analyze_log(log_path)
    
    if not abuses:
        return "No battery abuse detected. All parameters normal."
    
    report = ["🚨 BATTERY ABUSE REPORT 🚨", "="*40]
    for abuse in abuses:
        if isinstance(abuse, dict):
            report.append(
                f"[{abuse['timestamp']}] {abuse['type']}: "
                f"{abuse['message']}"
            )
        else:
            report.append(abuse)
    
    return "\n".join(report)

if __name__ == "__main__":
    print(generate_abuse_report())
