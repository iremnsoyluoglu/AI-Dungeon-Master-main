import React, { useState, useEffect } from "react";
import "./SaveLoadUI.css";

interface SaveLoadUIProps {
  characterId: string;
  characterName: string;
  onSave: (saveId: string) => void;
  onLoad: (saveId: string) => void;
  onClose: () => void;
}

interface SaveFile {
  save_id: string;
  timestamp: string;
  character_name: string;
  character_level: number;
  character_class: string;
  file_size: number;
}

const SaveLoadUI: React.FC<SaveLoadUIProps> = ({
  characterId,
  characterName,
  onSave,
  onLoad,
  onClose,
}) => {
  const [saveFiles, setSaveFiles] = useState<SaveFile[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedSave, setSelectedSave] = useState<string>("");
  const [saveName, setSaveName] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"save" | "load">("save");

  useEffect(() => {
    loadSaveFiles();
  }, [characterId]);

  const loadSaveFiles = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `/api/save/files?character_id=${characterId}`
      );
      if (response.ok) {
        const data = await response.json();
        setSaveFiles(data);
      }
    } catch (error) {
      console.error("Error loading save files:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (!saveName.trim()) {
      alert("Lütfen bir kayıt adı girin!");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("/api/save/game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          character_id: characterId,
          save_name: saveName,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          alert(`Oyun başarıyla kaydedildi: ${result.save_id}`);
          setSaveName("");
          loadSaveFiles();
        } else {
          alert(`Kaydetme hatası: ${result.error}`);
        }
      }
    } catch (error) {
      console.error("Error saving game:", error);
      alert("Kaydetme sırasında hata oluştu!");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoad = async () => {
    if (!selectedSave) {
      alert("Lütfen bir kayıt dosyası seçin!");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("/api/save/load", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          save_id: selectedSave,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          alert(`Oyun başarıyla yüklendi: ${result.character_name}`);
          onLoad(selectedSave);
          onClose();
        } else {
          alert(`Yükleme hatası: ${result.error}`);
        }
      }
    } catch (error) {
      console.error("Error loading game:", error);
      alert("Yükleme sırasında hata oluştu!");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (saveId: string) => {
    if (!confirm("Bu kayıt dosyasını silmek istediğinizden emin misiniz?")) {
      return;
    }

    try {
      const response = await fetch(`/api/save/delete`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ save_id: saveId }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          alert("Kayıt dosyası silindi!");
          loadSaveFiles();
        } else {
          alert(`Silme hatası: ${result.error}`);
        }
      }
    } catch (error) {
      console.error("Error deleting save:", error);
      alert("Silme sırasında hata oluştu!");
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp);
    return date.toLocaleString("tr-TR");
  };

  const getCharacterClassIcon = (characterClass: string): string => {
    const icons: { [key: string]: string } = {
      warrior: "⚔️",
      mage: "🔮",
      rogue: "🗡️",
      priest: "⛪",
      space_marine: "🛡️",
      tech_priest: "⚙️",
      inquisitor: "🔍",
      imperial_guard: "🎖️",
    };
    return icons[characterClass] || "👤";
  };

  return (
    <div className="save-load-overlay">
      <div className="save-load-modal">
        <div className="save-load-header">
          <h2>Kaydet / Yükle</h2>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="save-load-tabs">
          <button
            className={`tab-button ${activeTab === "save" ? "active" : ""}`}
            onClick={() => setActiveTab("save")}
          >
            💾 Kaydet
          </button>
          <button
            className={`tab-button ${activeTab === "load" ? "active" : ""}`}
            onClick={() => setActiveTab("load")}
          >
            📂 Yükle
          </button>
        </div>

        {activeTab === "save" && (
          <div className="save-section">
            <div className="save-form">
              <h3>Yeni Kayıt Oluştur</h3>
              <div className="form-group">
                <label>Kayıt Adı:</label>
                <input
                  type="text"
                  value={saveName}
                  onChange={(e) => setSaveName(e.target.value)}
                  placeholder="Kayıt adını girin..."
                  maxLength={50}
                />
              </div>
              <div className="character-info">
                <span>Karakter: {characterName}</span>
              </div>
              <button
                className="save-button"
                onClick={handleSave}
                disabled={isLoading || !saveName.trim()}
              >
                {isLoading ? "Kaydediliyor..." : "💾 Kaydet"}
              </button>
            </div>
          </div>
        )}

        {activeTab === "load" && (
          <div className="load-section">
            <h3>Mevcut Kayıtlar</h3>
            {isLoading ? (
              <div className="loading">Yükleniyor...</div>
            ) : saveFiles.length === 0 ? (
              <div className="no-saves">Henüz kayıt dosyası yok.</div>
            ) : (
              <div className="save-files">
                {saveFiles.map((save) => (
                  <div
                    key={save.save_id}
                    className={`save-file ${
                      selectedSave === save.save_id ? "selected" : ""
                    }`}
                    onClick={() => setSelectedSave(save.save_id)}
                  >
                    <div className="save-file-header">
                      <span className="character-icon">
                        {getCharacterClassIcon(save.character_class)}
                      </span>
                      <span className="character-name">
                        {save.character_name}
                      </span>
                      <span className="character-level">
                        Seviye {save.character_level}
                      </span>
                    </div>
                    <div className="save-file-details">
                      <span className="save-timestamp">
                        {formatTimestamp(save.timestamp)}
                      </span>
                      <span className="save-size">
                        {formatFileSize(save.file_size)}
                      </span>
                    </div>
                    <div className="save-file-actions">
                      <button
                        className="load-button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedSave(save.save_id);
                          handleLoad();
                        }}
                        disabled={isLoading}
                      >
                        📂 Yükle
                      </button>
                      <button
                        className="delete-button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(save.save_id);
                        }}
                        disabled={isLoading}
                      >
                        🗑️ Sil
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="save-load-footer">
          <button className="refresh-button" onClick={loadSaveFiles}>
            🔄 Yenile
          </button>
          <button
            className="auto-save-button"
            onClick={() => {
              // Auto-save functionality
              setSaveName(`Auto-Save ${new Date().toLocaleString("tr-TR")}`);
              handleSave();
            }}
          >
            ⚡ Otomatik Kaydet
          </button>
        </div>
      </div>
    </div>
  );
};

export default SaveLoadUI;
