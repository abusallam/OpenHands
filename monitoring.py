from typing import Dict, List
import time
import psutil
import prometheus_client as prom
from dataclasses import dataclass

@dataclass
class MCPMetrics:
    request_counter = prom.Counter('mcp_requests_total', 'Total MCP requests')
    edit_duration = prom.Histogram('mcp_edit_duration_seconds', 'Edit operation duration')
    validation_success = prom.Gauge('mcp_validation_success', 'Validation success rate')
    active_sessions = prom.Gauge('mcp_active_sessions', 'Number of active sessions')

class MetricsManager:
    def __init__(self):
        self.metrics = MCPMetrics()
        self.start_time = time.time()
        self.operation_timings: Dict[str, List[float]] = {}

    async def record_operation(self, operation_type: str, duration: float, success: bool):
        """Records operation metrics"""
        self.metrics.request_counter.inc()
        self.metrics.edit_duration.observe(duration)
        
        if operation_type not in self.operation_timings:
            self.operation_timings[operation_type] = []
        self.operation_timings[operation_type].append(duration)

    async def get_performance_metrics(self) -> Dict:
        """Gets current performance metrics"""
        return {
            "uptime": time.time() - self.start_time,
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,
            "operation_timings": {
                op: {
                    "avg": sum(times) / len(times),
                    "max": max(times),
                    "min": min(times)
                }
                for op, times in self.operation_timings.items()
            }
        } 