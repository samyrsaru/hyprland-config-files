#!/usr/bin/env python3

import sqlite3
import time
import datetime
import argparse
import os
import sys
from pathlib import Path

class BatteryMonitor:
    def __init__(self, db_path="./battery_history.db"):
        self.db_path = Path(db_path).expanduser()
        self.battery_path = Path("/sys/class/power_supply/BAT0")
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with battery history table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battery_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                capacity INTEGER NOT NULL,
                status TEXT NOT NULL,
                charge_now INTEGER,
                charge_full INTEGER,
                current_now INTEGER,
                voltage_now INTEGER,
                cycle_count INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    
    def read_battery_info(self):
        """Read current battery information from sysfs"""
        try:
            info = {}
            
            # Read capacity (percentage)
            with open(self.battery_path / "capacity") as f:
                info['capacity'] = int(f.read().strip())
            
            # Read status
            with open(self.battery_path / "status") as f:
                info['status'] = f.read().strip()
            
            # Read charge values
            with open(self.battery_path / "charge_now") as f:
                info['charge_now'] = int(f.read().strip())
            
            with open(self.battery_path / "charge_full") as f:
                info['charge_full'] = int(f.read().strip())
            
            # Read current (may not always be available)
            try:
                with open(self.battery_path / "current_now") as f:
                    info['current_now'] = int(f.read().strip())
            except:
                info['current_now'] = None
            
            # Read voltage
            try:
                with open(self.battery_path / "voltage_now") as f:
                    info['voltage_now'] = int(f.read().strip())
            except:
                info['voltage_now'] = None
            
            # Read cycle count
            try:
                with open(self.battery_path / "cycle_count") as f:
                    info['cycle_count'] = int(f.read().strip())
            except:
                info['cycle_count'] = None
            
            return info
        except Exception as e:
            print(f"Error reading battery info: {e}")
            return None
    
    def record_battery_data(self):
        """Record current battery data to database"""
        info = self.read_battery_info()
        if not info:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = int(time.time())
        cursor.execute('''
            INSERT INTO battery_history 
            (timestamp, capacity, status, charge_now, charge_full, current_now, voltage_now, cycle_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            info['capacity'],
            info['status'],
            info['charge_now'],
            info['charge_full'],
            info['current_now'],
            info['voltage_now'],
            info['cycle_count']
        ))
        
        conn.commit()
        conn.close()
        return True
    
    def get_history(self, hours=24, limit=None):
        """Get battery history for specified hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_timestamp = int(time.time()) - (hours * 3600)
        
        query = '''
            SELECT timestamp, capacity, status, charge_now, charge_full, current_now, voltage_now, cycle_count
            FROM battery_history 
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query, (since_timestamp,))
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_statistics(self, hours=24):
        """Get battery statistics for specified period"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_timestamp = int(time.time()) - (hours * 3600)
        
        cursor.execute('''
            SELECT 
                AVG(capacity) as avg_capacity,
                MIN(capacity) as min_capacity,
                MAX(capacity) as max_capacity,
                COUNT(*) as record_count
            FROM battery_history 
            WHERE timestamp >= ?
        ''', (since_timestamp,))
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'avg_capacity': stats[0],
            'min_capacity': stats[1],
            'max_capacity': stats[2],
            'record_count': stats[3]
        }
    
    def monitor_continuous(self, interval=300):
        """Continuously monitor battery and record data"""
        print(f"Starting battery monitoring (interval: {interval}s)")
        print(f"Database: {self.db_path}")
        
        try:
            while True:
                if self.record_battery_data():
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    info = self.read_battery_info()
                    print(f"[{now}] Recorded: {info['capacity']}% ({info['status']})")
                else:
                    print(f"[{now}] Failed to record battery data")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

def format_timestamp(timestamp):
    """Format Unix timestamp to readable string"""
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def main():
    parser = argparse.ArgumentParser(description="Battery History Monitor")
    parser.add_argument('--monitor', action='store_true', 
                       help='Start continuous monitoring')
    parser.add_argument('--interval', type=int, default=300,
                       help='Monitoring interval in seconds (default: 300)')
    parser.add_argument('--history', type=int, default=24,
                       help='Show history for last N hours (default: 24)')
    parser.add_argument('--limit', type=int,
                       help='Limit number of history records shown')
    parser.add_argument('--stats', action='store_true',
                       help='Show battery statistics')
    parser.add_argument('--current', action='store_true',
                       help='Show current battery info and record it')
    
    args = parser.parse_args()
    
    monitor = BatteryMonitor()
    
    if args.monitor:
        monitor.monitor_continuous(args.interval)
    elif args.current:
        info = monitor.read_battery_info()
        if info:
            print(f"Current Battery Status:")
            print(f"  Capacity: {info['capacity']}%")
            print(f"  Status: {info['status']}")
            print(f"  Charge: {info['charge_now']:,} / {info['charge_full']:,} µAh")
            if info['current_now']:
                print(f"  Current: {info['current_now']:,} µA")
            if info['voltage_now']:
                print(f"  Voltage: {info['voltage_now']/1000000:.2f} V")
            if info['cycle_count']:
                print(f"  Cycle Count: {info['cycle_count']}")
            
            monitor.record_battery_data()
            print("\nData recorded to database.")
    elif args.stats:
        stats = monitor.get_statistics(args.history)
        print(f"Battery Statistics (last {args.history} hours):")
        print(f"  Records: {stats['record_count']}")
        if stats['avg_capacity']:
            print(f"  Average Capacity: {stats['avg_capacity']:.1f}%")
            print(f"  Min Capacity: {stats['min_capacity']}%")
            print(f"  Max Capacity: {stats['max_capacity']}%")
        else:
            print("  No data available for this period")
    else:
        # Show history
        history = monitor.get_history(args.history, args.limit)
        if history:
            print(f"Battery History (last {args.history} hours):")
            print("Time                 Capacity Status      Charge (µAh)")
            print("-" * 60)
            for record in history:
                timestamp, capacity, status, charge_now, charge_full, current_now, voltage_now, cycle_count = record
                time_str = format_timestamp(timestamp)
                charge_str = f"{charge_now:,}/{charge_full:,}" if charge_now and charge_full else "N/A"
                print(f"{time_str} {capacity:3d}%     {status:12} {charge_str}")
        else:
            print(f"No battery history found for last {args.history} hours")

if __name__ == "__main__":
    main()
