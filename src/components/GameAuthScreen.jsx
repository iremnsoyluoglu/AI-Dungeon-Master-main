import React, { useState } from "react";

export default function GameAuthScreen({ onAuthenticated }) {
  const [activeTab, setActiveTab] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = () => {
    if (formData.username && formData.password) {
      onAuthenticated();
    } else {
      alert("Lütfen kullanıcı adı ve şifre giriniz!");
    }
  };

  const handleGuestLogin = () => {
    onAuthenticated();
  };

  return (
    <div className="auth-screen">
      <div className="auth-panel">
        {/* Header */}
        <div className="auth-header">
          <div className="gamepad-icon">🎮+</div>
          <h1 className="auth-title">AI DUNGEON MASTER</h1>
          <p className="auth-subtitle">Fantastik Dünyalara Açılan Kapı</p>
        </div>

        {/* Tabs */}
        <div className="auth-tabs">
          <button
            className={`tab-button ${activeTab === 0 ? "active" : ""}`}
            onClick={() => setActiveTab(0)}
          >
            GİRİŞ
          </button>
          <button
            className={`tab-button ${activeTab === 1 ? "active" : ""}`}
            onClick={() => setActiveTab(1)}
          >
            KAYIT
          </button>
          <button
            className={`tab-button ${activeTab === 2 ? "active" : ""}`}
            onClick={() => setActiveTab(2)}
          >
            MİSAFİR
          </button>
        </div>

        {/* Login Form */}
        {activeTab === 0 && (
          <div className="auth-form">
            <div className="input-group">
              <span className="input-icon">👤</span>
              <input
                type="text"
                name="username"
                placeholder="Kullanıcı Adı"
                value={formData.username}
                onChange={handleInputChange}
                className="auth-input"
              />
            </div>
            <div className="input-group">
              <span className="input-icon">🔒</span>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Şifre"
                value={formData.password}
                onChange={handleInputChange}
                className="auth-input"
              />
              <button
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "👁️" : "👁️‍🗨️"}
              </button>
            </div>
            <button className="login-button" onClick={handleLogin}>
              GİRİŞ YAP
            </button>
          </div>
        )}

        {/* Register Form */}
        {activeTab === 1 && (
          <div className="auth-form">
            <div className="input-group">
              <span className="input-icon">👤</span>
              <input
                type="text"
                name="username"
                placeholder="Kullanıcı Adı"
                value={formData.username}
                onChange={handleInputChange}
                className="auth-input"
              />
            </div>
            <div className="input-group">
              <span className="input-icon">📧</span>
              <input
                type="email"
                name="email"
                placeholder="E-posta"
                className="auth-input"
              />
            </div>
            <div className="input-group">
              <span className="input-icon">🔒</span>
              <input
                type="password"
                name="password"
                placeholder="Şifre"
                className="auth-input"
              />
            </div>
            <div className="input-group">
              <span className="input-icon">🔒</span>
              <input
                type="password"
                name="confirmPassword"
                placeholder="Şifre Tekrar"
                className="auth-input"
              />
            </div>
            <button className="login-button">KAYIT OL</button>
          </div>
        )}

        {/* Guest Form */}
        {activeTab === 2 && (
          <div className="auth-form">
            <div className="guest-info">
              <div className="guest-icon">🌟</div>
              <h3>Misafir Modu</h3>
              <p>Hemen oyuna başla, karakter oluştur ve maceraya atıl!</p>
            </div>
            <button className="login-button" onClick={handleGuestLogin}>
              MİSAFİR OLARAK BAŞLA
            </button>
          </div>
        )}
      </div>

      <style jsx>{`
        .auth-screen {
          min-height: 100vh;
          background: linear-gradient(135deg, #0d1117 0%, #1c2128 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }

        .auth-panel {
          background: rgba(28, 33, 40, 0.95);
          border: 1px solid #ffc107;
          border-radius: 12px;
          padding: 2rem;
          width: 100%;
          max-width: 400px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .auth-header {
          text-align: center;
          margin-bottom: 2rem;
        }

        .gamepad-icon {
          font-size: 3rem;
          color: #ffc107;
          margin-bottom: 1rem;
        }

        .auth-title {
          color: #ffc107;
          font-size: 1.8rem;
          font-weight: bold;
          margin: 0 0 0.5rem 0;
          text-shadow: 0 0 10px rgba(255, 193, 7, 0.5);
        }

        .auth-subtitle {
          color: #8b949e;
          font-size: 0.9rem;
          margin: 0;
        }

        .auth-tabs {
          display: flex;
          margin-bottom: 2rem;
          border-bottom: 1px solid #333;
        }

        .tab-button {
          flex: 1;
          background: none;
          border: none;
          color: #8b949e;
          padding: 1rem;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
        }

        .tab-button.active {
          color: #ffc107;
          font-weight: bold;
        }

        .tab-button.active::after {
          content: "";
          position: absolute;
          bottom: -1px;
          left: 0;
          right: 0;
          height: 2px;
          background: #ffc107;
        }

        .auth-form {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .input-group {
          position: relative;
          display: flex;
          align-items: center;
        }

        .input-icon {
          position: absolute;
          left: 12px;
          color: #8b949e;
          font-size: 1.1rem;
          z-index: 1;
        }

        .auth-input {
          width: 100%;
          padding: 12px 12px 12px 40px;
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid #333;
          border-radius: 6px;
          color: white;
          font-size: 1rem;
          outline: none;
          transition: border-color 0.3s ease;
        }

        .auth-input:focus {
          border-color: #ffc107;
        }

        .auth-input::placeholder {
          color: #8b949e;
        }

        .password-toggle {
          position: absolute;
          right: 12px;
          background: none;
          border: none;
          color: #8b949e;
          cursor: pointer;
          font-size: 1.1rem;
          z-index: 1;
        }

        .login-button {
          background: #ffc107;
          color: #1c2128;
          border: none;
          border-radius: 6px;
          padding: 12px;
          font-size: 1rem;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.3s ease;
          margin-top: 1rem;
        }

        .login-button:hover {
          background: #e6a000;
          transform: translateY(-2px);
          box-shadow: 0 4px 15px rgba(255, 193, 7, 0.4);
        }

        .guest-info {
          text-align: center;
          margin-bottom: 1rem;
        }

        .guest-icon {
          font-size: 3rem;
          color: #ffc107;
          margin-bottom: 1rem;
        }

        .guest-info h3 {
          color: #ffc107;
          margin: 0 0 0.5rem 0;
        }

        .guest-info p {
          color: #8b949e;
          margin: 0;
          font-size: 0.9rem;
        }
      `}</style>
    </div>
  );
}
