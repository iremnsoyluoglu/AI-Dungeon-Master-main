class LLMComicTrainer {
  // Comic okuma prompt'u oluştur
  createComicReadingPrompt(comicData) {
    return `
TASK: Bu çizgi romanı analiz et ve RPG senaryo yazımı için öğren.

COMIC: ${comicData.title} (${comicData.genre})

PAGES DATA:
${comicData.pages
  .map(
    (page) => `
Page ${page.pageNumber}:
Panel Descriptions: ${page.panelDescriptions.join(" | ")}
Dialogue: ${page.characterDialogue
      .map((d) => `${d.character}: "${d.text}"`)
      .join(" / ")}
Text: ${page.extractedText}
`
  )
  .join("\n")}

ANALYSIS TASKS:
1. Karakter gelişimi ve motivasyonları
2. Hikaye yapısı ve pacing
3. Savaş sahneleri ve aksiyon sekansları
4. Diyalog yazımı ve karakter sesleri
5. FRP mekanikleri (zar atışları, skill check'ler, initiative, round-based combat, status effects, multi-enemy/multi-round combat)
6. Karar noktaları ve branching paths
7. Atmosfer ve mood yaratma
8. NPC etkileşimleri

OUTPUT FORMAT:
TITLE: [Comic başlığı]
GENRE: [Tür]
ANALYSIS:
- Character Development: [karakter gelişimi analizi]
- Story Structure: [hikaye yapısı analizi]
- Combat Scenes: [savaş sahneleri analizi]
- Dialogue: [diyalog analizi]
- FRP Mechanics: [FRP mekanikleri analizi]
- Decision Points: [karar noktaları analizi]
- Atmosphere: [atmosfer analizi]
- NPC Interactions: [NPC etkileşimleri analizi]

LEARNED TECHNIQUES:
- [Teknik 1]
- [Teknik 2]
- [Teknik 3]
- [Teknik 4]

KNOWLEDGE BASE:
[Öğrenilen bilgilerin özeti]
`;
  }

  // Senaryo üretme prompt'u oluştur
  createScenarioGenerationPrompt(theme, difficulty, knowledgeBase) {
    return `
TASK: ${theme} temalı, ${difficulty} zorlukta RPG senaryosu üret.

ÖĞRENİLEN BİLGİLER:
${knowledgeBase}

SENARYO GEREKSİNİMLERİ:
- Tema: ${theme}
- Zorluk: ${difficulty}
- Öğrenilen teknikleri kullan
- FRP mekanikleri ekle (zar atışları, skill check'ler, initiative, round-based combat, status effects)
- NPC etkileşimleri olsun
- Karar noktaları olsun
- Savaş sistemi olsun
- Atmosfer yarat

OUTPUT FORMAT:
TITLE: [Senaryo başlığı]
THEME: [tema]
DIFFICULTY: [zorluk]
DESCRIPTION: [Senaryo açıklaması]

SCENES:
- Scene 1: [başlık]
  Description: [açıklama]
  NPCs: [NPC listesi]
  Decision Points: [karar noktaları]
  Combat: [savaş bilgisi]
  Dice Rolls: [zar atışları]

CHOICES:
- [Seçenek 1]
- [Seçenek 2]
- [Seçenek 3]

FRP MECHANICS:
- Dice Types: [kullanılacak zar tipleri]
- Skill Checks: [beceri kontrolleri]
- Combat System: [savaş sistemi]
- Status Effects: [durum etkileri]
`;
  }
}

module.exports = { LLMComicTrainer }; 