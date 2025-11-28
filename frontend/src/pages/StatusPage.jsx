import { useEffect, useState, useCallback } from "react";
import { getServicesStatus } from "../services/apiClient";
import "../styles/StatusPage.css";

export default function StatusPage() {
  const [services, setServices] = useState([]);
  const [overall, setOverall] = useState("loading");
  const [expanded, setExpanded] = useState({});
  const [tooltip, setTooltip] = useState({
    visible: false,
    text: "",
    x: 0,
    y: 0,
  });

  const fetchStatus = useCallback(async () => {
    try {
      const res = await getServicesStatus(); // Usa overall_status + checks

      const formatted = res.checks.map((c) => ({
        service_name: c.component,
        status: c.status === "OK" ? "OK" : "Down",
      }));

      setServices(formatted);

      if (res.overall_status === "Available") {
        setOverall("ok");
      } else if (res.overall_status === "Unavailable") {
        setOverall("down");
      } else {
        setOverall("partial");
      }
    } catch {
      setOverall("down");
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return (
    <div className="status-page">
      <div className="main-icon">
        {overall === "ok" && "☁️✨"}
        {overall === "partial" && "⛅⚠️"}
        {overall === "down" && "🌩️❌"}
      </div>
      
      <h1 className="main-title">
        {overall === "ok" && "All services are online"}
        {overall === "down" && "All services are down"}
        {overall === "partial" && "Some services are partially available"}
      </h1>

      <p className="updated-text">
        Last updated on {new Date().toLocaleTimeString()}
      </p>

      <div className="status-container-card">
        {services.map((service, index) => {
          const isOpen = expanded[index];

          return (
            <div key={index} className="status-row">
              <div
                className="status-header-row"
                onClick={() =>
                  setExpanded((prev) => ({ ...prev, [index]: !prev[index] }))
                }
              >
                <span className="service-name-row">
                  ✅ {service.service_name}
                </span>
                <span
                  className={`service-status-badge ${
                    service.status === "OK" ? "ok" : "down"
                  }`}
                >
                  {service.status === "OK" ? "Operational" : "Down"}
                </span>
              </div>

              {isOpen && (
                <div className="accordion-content">
                  <div className="service-metrics">
                    <span className="last-updated">
                      Last updated: {new Date().toLocaleTimeString()}
                    </span>
                  </div>

                  <div
                    className="service-bar"
                    onMouseEnter={(e) =>
                      setTooltip({
                        visible: true,
                        text:
                          service.status === "OK"
                            ? "Today · 200 OK · Operational"
                            : "Today · 500 Error · Unavailable",
                        x: e.clientX,
                        y: e.clientY,
                      })
                    }
                    onMouseLeave={() =>
                      setTooltip({ visible: false, text: "", x: 0, y: 0 })
                    }
                  >
                    <div
                      className={`status-bar ${
                        service.status === "OK" ? "ok" : "down"
                      }`}
                    ></div>
                  </div>

                  <div className="bar-label">Today</div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {tooltip.visible && (
        <div
          className="tooltip"
          style={{
            position: "fixed",
            top: tooltip.y + 10,
            left: tooltip.x + 10,
            background: "#333",
            color: "#fff",
            padding: "4px 8px",
            borderRadius: "4px",
            fontSize: "0.8rem",
            zIndex: 1000,
            pointerEvents: "none",
          }}
        >
          {tooltip.text}
        </div>
      )}

      <footer className="footer">Powered by Dropi 🧡</footer>
    </div>
  );
}
