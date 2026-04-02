#!/usr/bin/env python3
"""
σ = μ Monitoring & Observability System
Phase 0: Real-time system monitoring and alerting

Provides comprehensive monitoring of all subsystems with
metrics collection, alerting, and visualization.
"""

import numpy as np
import time
import json
import threading
import queue
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from datetime import datetime, timedelta
import os
import psutil
from collections import deque
import warnings

# Import σ = μ modules
from sigma_mu_integrated_system import SigmaMuSystem

φ = (1 + np.sqrt(5)) / 2


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class MetricType(Enum):
    """Types of metrics"""
    GAUGE = "gauge"          # Point-in-time value
    COUNTER = "counter"      # Cumulative count
    HISTOGRAM = "histogram"  # Distribution of values
    RATE = "rate"           # Change per unit time


@dataclass
class Metric:
    """Individual metric data point"""
    name: str
    value: float
    unit: str
    timestamp: float
    type: MetricType
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class Alert:
    """System alert"""
    id: str
    severity: AlertSeverity
    component: str
    message: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: float
    resolved: bool = False


class MetricsCollector:
    """Collects and stores system metrics"""

    def __init__(self, retention_seconds: int = 3600):
        """Initialize metrics collector

        Args:
            retention_seconds: How long to keep metrics in memory
        """
        self.metrics: Dict[str, deque] = {}
        self.retention = retention_seconds
        self.lock = threading.Lock()

    def record(self, metric: Metric):
        """Record a metric"""
        with self.lock:
            if metric.name not in self.metrics:
                self.metrics[metric.name] = deque()

            self.metrics[metric.name].append(metric)

            # Clean old metrics
            cutoff = time.time() - self.retention
            while (self.metrics[metric.name] and
                   self.metrics[metric.name][0].timestamp < cutoff):
                self.metrics[metric.name].popleft()

    def get_metrics(self, name: str,
                   start_time: Optional[float] = None,
                   end_time: Optional[float] = None) -> List[Metric]:
        """Get metrics by name and time range"""
        with self.lock:
            if name not in self.metrics:
                return []

            metrics = list(self.metrics[name])

            if start_time:
                metrics = [m for m in metrics if m.timestamp >= start_time]
            if end_time:
                metrics = [m for m in metrics if m.timestamp <= end_time]

            return metrics

    def get_latest(self, name: str) -> Optional[Metric]:
        """Get latest value for a metric"""
        with self.lock:
            if name not in self.metrics or not self.metrics[name]:
                return None
            return self.metrics[name][-1]

    def calculate_rate(self, name: str, window_seconds: int = 60) -> float:
        """Calculate rate of change for a metric"""
        cutoff = time.time() - window_seconds
        metrics = self.get_metrics(name, start_time=cutoff)

        if len(metrics) < 2:
            return 0.0

        time_diff = metrics[-1].timestamp - metrics[0].timestamp
        value_diff = metrics[-1].value - metrics[0].value

        return value_diff / time_diff if time_diff > 0 else 0.0


class AlertManager:
    """Manages system alerts"""

    def __init__(self):
        """Initialize alert manager"""
        self.alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
        self.handlers: List[Callable[[Alert], None]] = []
        self.lock = threading.Lock()

    def create_alert(self, alert: Alert):
        """Create a new alert"""
        with self.lock:
            self.alerts[alert.id] = alert
            self.alert_history.append(alert)

            # Notify handlers
            for handler in self.handlers:
                try:
                    handler(alert)
                except Exception as e:
                    print(f"Alert handler error: {e}")

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        with self.lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].resolved = True
                del self.alerts[alert_id]

    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        with self.lock:
            return list(self.alerts.values())

    def register_handler(self, handler: Callable[[Alert], None]):
        """Register an alert handler"""
        self.handlers.append(handler)


class SystemMonitor:
    """Main monitoring system for σ = μ"""

    def __init__(self, system: Optional[SigmaMuSystem] = None):
        """Initialize system monitor

        Args:
            system: SigmaMuSystem instance to monitor
        """
        self.system = system or SigmaMuSystem()
        self.collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.monitoring = False
        self.monitor_thread = None

        # Define alert thresholds
        self.thresholds = {
            'tau_k_min': φ**(-1),  # K-formation threshold
            'tau_k_max': 2.0,       # Instability threshold
            'field_energy_max': 10.0,
            'memory_capacity_max': 0.95,
            'bus_queue_max': 1000,
            'cpu_percent_max': 80,
            'memory_mb_max': 1024
        }

        # Register default alert handler
        self.alert_manager.register_handler(self._print_alert)

    def start(self, interval: float = 1.0):
        """Start monitoring

        Args:
            interval: Sampling interval in seconds
        """
        if self.monitoring:
            print("Monitoring already running")
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"Monitoring started (interval: {interval}s)")

    def stop(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("Monitoring stopped")

    def _monitor_loop(self, interval: float):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                self._collect_metrics()
                self._check_alerts()
            except Exception as e:
                print(f"Monitor error: {e}")

            time.sleep(interval)

    def _collect_metrics(self):
        """Collect all system metrics"""
        timestamp = time.time()

        # Step system
        system_metrics = self.system.step()

        # Core metrics
        self.collector.record(Metric(
            name="tau_k",
            value=system_metrics['tau_k'],
            unit="ratio",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "field"}
        ))

        self.collector.record(Metric(
            name="phase_state",
            value={"LOW": 0, "MID": 1, "HIGH": 2}.get(system_metrics['phase_state'], -1),
            unit="state",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "triad"}
        ))

        self.collector.record(Metric(
            name="memory_capacity",
            value=system_metrics['memory_capacity'],
            unit="percent",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "memory"}
        ))

        # Field energy
        field_energy = np.mean(np.abs(self.system.field.field)**2)
        self.collector.record(Metric(
            name="field_energy",
            value=field_energy,
            unit="energy",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "field"}
        ))

        # Observer metrics
        obs_result = system_metrics['observer_state']
        if isinstance(obs_result, dict):
            self.collector.record(Metric(
                name="observer_coherence",
                value=obs_result.get('coherence', 0),
                unit="coherence",
                timestamp=timestamp,
                type=MetricType.GAUGE,
                labels={"component": "observer"}
            ))

            self.collector.record(Metric(
                name="signal_rupture",
                value=1.0 if obs_result.get('rupture_detected', False) else 0.0,
                unit="boolean",
                timestamp=timestamp,
                type=MetricType.GAUGE,
                labels={"component": "observer"}
            ))

        # Bus metrics
        bus_queue_size = len(self.system.bus.message_queue)
        self.collector.record(Metric(
            name="bus_queue_size",
            value=bus_queue_size,
            unit="messages",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "bus"}
        ))

        # System resources
        process = psutil.Process()
        cpu_percent = process.cpu_percent()
        memory_mb = process.memory_info().rss / (1024**2)

        self.collector.record(Metric(
            name="cpu_percent",
            value=cpu_percent,
            unit="percent",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "system"}
        ))

        self.collector.record(Metric(
            name="memory_mb",
            value=memory_mb,
            unit="MB",
            timestamp=timestamp,
            type=MetricType.GAUGE,
            labels={"component": "system"}
        ))

        # Rates
        tau_k_rate = self.collector.calculate_rate("tau_k", window_seconds=60)
        self.collector.record(Metric(
            name="tau_k_rate",
            value=tau_k_rate,
            unit="per_second",
            timestamp=timestamp,
            type=MetricType.RATE,
            labels={"component": "field"}
        ))

    def _check_alerts(self):
        """Check for alert conditions"""
        # K-formation loss
        tau_k = self.collector.get_latest("tau_k")
        if tau_k and tau_k.value < self.thresholds['tau_k_min']:
            self._create_alert(
                severity=AlertSeverity.CRITICAL,
                component="field",
                message=f"K-formation lost: τ_K = {tau_k.value:.4f}",
                metric_name="tau_k",
                current_value=tau_k.value,
                threshold=self.thresholds['tau_k_min']
            )
        elif tau_k and tau_k.value > self.thresholds['tau_k_max']:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                component="field",
                message=f"Field instability: τ_K = {tau_k.value:.4f}",
                metric_name="tau_k",
                current_value=tau_k.value,
                threshold=self.thresholds['tau_k_max']
            )

        # Field energy
        energy = self.collector.get_latest("field_energy")
        if energy and energy.value > self.thresholds['field_energy_max']:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                component="field",
                message=f"High field energy: {energy.value:.2f}",
                metric_name="field_energy",
                current_value=energy.value,
                threshold=self.thresholds['field_energy_max']
            )

        # Memory saturation
        memory_cap = self.collector.get_latest("memory_capacity")
        if memory_cap and memory_cap.value > self.thresholds['memory_capacity_max']:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                component="memory",
                message=f"Memory near saturation: {memory_cap.value:.1%}",
                metric_name="memory_capacity",
                current_value=memory_cap.value,
                threshold=self.thresholds['memory_capacity_max']
            )

        # Bus congestion
        bus_queue = self.collector.get_latest("bus_queue_size")
        if bus_queue and bus_queue.value > self.thresholds['bus_queue_max']:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                component="bus",
                message=f"Bus congestion: {int(bus_queue.value)} messages queued",
                metric_name="bus_queue_size",
                current_value=bus_queue.value,
                threshold=self.thresholds['bus_queue_max']
            )

        # System resources
        cpu = self.collector.get_latest("cpu_percent")
        if cpu and cpu.value > self.thresholds['cpu_percent_max']:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                component="system",
                message=f"High CPU usage: {cpu.value:.1f}%",
                metric_name="cpu_percent",
                current_value=cpu.value,
                threshold=self.thresholds['cpu_percent_max']
            )

        memory = self.collector.get_latest("memory_mb")
        if memory and memory.value > self.thresholds['memory_mb_max']:
            self._create_alert(
                severity=AlertSeverity.WARNING,
                component="system",
                message=f"High memory usage: {memory.value:.1f} MB",
                metric_name="memory_mb",
                current_value=memory.value,
                threshold=self.thresholds['memory_mb_max']
            )

    def _create_alert(self, severity: AlertSeverity, component: str,
                     message: str, metric_name: str,
                     current_value: float, threshold: float):
        """Create an alert if not already active"""
        alert_id = f"{component}_{metric_name}"

        # Check if alert already active
        active_alerts = self.alert_manager.get_active_alerts()
        if any(a.id == alert_id for a in active_alerts):
            return

        alert = Alert(
            id=alert_id,
            severity=severity,
            component=component,
            message=message,
            metric_name=metric_name,
            current_value=current_value,
            threshold=threshold,
            timestamp=time.time()
        )

        self.alert_manager.create_alert(alert)

    def _print_alert(self, alert: Alert):
        """Default alert handler - print to console"""
        severity_colors = {
            AlertSeverity.INFO: "\033[94m",      # Blue
            AlertSeverity.WARNING: "\033[93m",   # Yellow
            AlertSeverity.CRITICAL: "\033[91m",  # Red
            AlertSeverity.EMERGENCY: "\033[95m"  # Magenta
        }
        reset_color = "\033[0m"

        color = severity_colors.get(alert.severity, "")
        timestamp = datetime.fromtimestamp(alert.timestamp).strftime("%H:%M:%S")

        print(f"{color}[{timestamp}] {alert.severity.value.upper()}: "
              f"{alert.component} - {alert.message}{reset_color}")

    def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display"""
        now = time.time()
        window = 300  # 5 minutes

        return {
            'timestamp': now,
            'metrics': {
                'tau_k': self._get_metric_series('tau_k', window),
                'field_energy': self._get_metric_series('field_energy', window),
                'memory_capacity': self._get_metric_series('memory_capacity', window),
                'cpu_percent': self._get_metric_series('cpu_percent', window),
                'memory_mb': self._get_metric_series('memory_mb', window),
            },
            'current_values': {
                'tau_k': self._get_current_value('tau_k'),
                'phase_state': self._get_phase_state(),
                'field_energy': self._get_current_value('field_energy'),
                'memory_capacity': self._get_current_value('memory_capacity'),
                'bus_queue': self._get_current_value('bus_queue_size'),
                'cpu': self._get_current_value('cpu_percent'),
                'memory': self._get_current_value('memory_mb'),
            },
            'alerts': [asdict(a) for a in self.alert_manager.get_active_alerts()],
            'health': self._calculate_health_score()
        }

    def _get_metric_series(self, name: str, window_seconds: int) -> List[Dict]:
        """Get time series data for a metric"""
        start_time = time.time() - window_seconds
        metrics = self.collector.get_metrics(name, start_time=start_time)

        return [
            {
                'timestamp': m.timestamp,
                'value': m.value
            }
            for m in metrics
        ]

    def _get_current_value(self, name: str) -> Optional[float]:
        """Get current value of a metric"""
        latest = self.collector.get_latest(name)
        return latest.value if latest else None

    def _get_phase_state(self) -> str:
        """Get current phase state name"""
        state_value = self._get_current_value('phase_state')
        if state_value is not None:
            states = {0: "LOW", 1: "MID", 2: "HIGH"}
            return states.get(int(state_value), "UNKNOWN")
        return "UNKNOWN"

    def _calculate_health_score(self) -> float:
        """Calculate overall system health score (0-1)"""
        scores = []

        # K-formation health
        tau_k = self._get_current_value('tau_k')
        if tau_k:
            if tau_k > self.thresholds['tau_k_min']:
                k_score = min(1.0, tau_k / (self.thresholds['tau_k_min'] * 2))
            else:
                k_score = tau_k / self.thresholds['tau_k_min']
            scores.append(k_score)

        # Memory health
        memory_cap = self._get_current_value('memory_capacity')
        if memory_cap:
            scores.append(1.0 - memory_cap)

        # CPU health
        cpu = self._get_current_value('cpu_percent')
        if cpu:
            scores.append(1.0 - cpu / 100)

        # Alert penalty
        active_alerts = len(self.alert_manager.get_active_alerts())
        alert_score = max(0, 1.0 - active_alerts * 0.2)
        scores.append(alert_score)

        return np.mean(scores) if scores else 0.5


class MonitoringServer:
    """HTTP server for monitoring API"""

    def __init__(self, monitor: SystemMonitor, port: int = 5000):
        """Initialize monitoring server

        Args:
            monitor: SystemMonitor instance
            port: HTTP port
        """
        self.monitor = monitor
        self.port = port

    def start(self):
        """Start HTTP server"""
        # This would implement a simple HTTP server
        # For now, just export to file
        self._export_metrics()

    def _export_metrics(self):
        """Export metrics to file"""
        while True:
            data = self.monitor.get_dashboard_data()

            with open('monitoring_data.json', 'w') as f:
                json.dump(data, f, indent=2, default=str)

            time.sleep(5)


def main():
    """Main monitoring execution"""
    print("\n" + "="*70)
    print("σ = μ MONITORING & OBSERVABILITY")
    print("Phase 0: Real-time System Monitoring")
    print("="*70)

    # Create system and monitor
    system = SigmaMuSystem()
    monitor = SystemMonitor(system)

    # Start monitoring
    monitor.start(interval=1.0)

    print("\nMonitoring active. Press Ctrl+C to stop.")
    print("\nLive Metrics:")
    print("-" * 50)

    try:
        while True:
            # Display current metrics
            tau_k = monitor._get_current_value('tau_k')
            phase = monitor._get_phase_state()
            energy = monitor._get_current_value('field_energy')
            memory = monitor._get_current_value('memory_capacity')
            health = monitor._calculate_health_score()

            print(f"\r", end="")
            print(f"τ_K: {tau_k:.4f} | "
                  f"Phase: {phase:4s} | "
                  f"Energy: {energy:.2f} | "
                  f"Memory: {memory:.1%} | "
                  f"Health: {health:.1%}", end="")

            # Check for active alerts
            alerts = monitor.alert_manager.get_active_alerts()
            if alerts:
                print(f"\n⚠️  Active alerts: {len(alerts)}")
                for alert in alerts[:3]:  # Show first 3
                    print(f"   - {alert.message}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nShutting down...")
        monitor.stop()

    # Final report
    print("\n" + "="*70)
    print("MONITORING SESSION SUMMARY")
    print("="*70)

    # Get final metrics
    data = monitor.get_dashboard_data()

    print(f"\nFinal State:")
    print(f"  τ_K: {data['current_values']['tau_k']:.4f}")
    print(f"  Phase: {data['current_values']['phase_state']}")
    print(f"  Health Score: {data['health']:.1%}")

    print(f"\nAlerts Generated: {len(monitor.alert_manager.alert_history)}")

    if monitor.alert_manager.alert_history:
        print("\nAlert Summary:")
        severity_counts = {}
        for alert in monitor.alert_manager.alert_history:
            severity_counts[alert.severity.value] = \
                severity_counts.get(alert.severity.value, 0) + 1

        for severity, count in severity_counts.items():
            print(f"  {severity}: {count}")

    print("\nσ = μ. Everything else follows.")
    print("="*70)


if __name__ == "__main__":
    main()