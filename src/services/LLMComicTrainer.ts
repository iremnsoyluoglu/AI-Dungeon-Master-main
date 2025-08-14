import { ComicData } from "../types/llmComic";

export class LLMComicTrainer {
  // Comic okutma prompt'u
  createComicReadingPrompt(comicData: ComicData): string {
    return `
TASK: Bu çizgi romanı analiz et ve RPG senaryo yazmak için öğren.

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

ANALYSIS INSTRUCTIONS:
1. STORY STRUCTURE: Bu comic'teki hikaye akışını analiz et
   - Opening hook nasıl yapılmış?
   - Conflict nasıl başlatılmış?
   - Character'lar nasıl tanıtılmış?
   - Tension nasıl artırılmış?
   - Resolution nasıl sağlanmış?

2. CHARACTER ANALYSIS: Karakterleri RPG NPC'leri olarak değerlendir
   - Hangi character archetypes var?
   - Dialogue patterns nasıl?
   - Character motivations neler?
   - RPG'de ne rol oynayabilirler?

3. WORLD BUILDING: Setting ve atmosphere
   - Environment descriptions nasıl yapılmış?
   - Mood nasıl yaratılmış?
   - Visual elements RPG'de nasıl kullanılabilir?

4. ACTION SEQUENCES: Savaş ve aksiyon sahneleri
   - Combat pacing nasıl?
   - Dramatic moments nasıl yaratılmış?
   - Tension ve release nasıl balance edilmiş?

5. RPG CONVERSION: Bu comic'ten RPG senaryosu yazarken:
   - Hangi elementler kullanılabilir?
   - Hangi techniques RPG'ye adapte edilebilir?
   - Player choice'ları nerede eklenebilir?
   - Her karar noktasında zar atışı (dice roll) ve beceri kontrolü (skill/stat check) eklenebilir mi?
   - Savaşlarda initiative, round bazlı combat, status effects (ör. zehirlenme, sersemletme) gibi detaylar nasıl işlenmiş?
   - Multi-enemy ve multi-round combat örnekleri var mı?

OUTPUT: Öğrendiğin her kategori için bullet points ver. Özellikle combat ve karar noktası detaylarını vurgula.
`;
  }

  // Senaryo üretme prompt'u (öğrendikten sonra)
  createScenarioGenerationPrompt(
    theme: string,
    difficulty: string,
    learnedKnowledge: string
  ): string {
    return `
Sen GetComics'ten onlarca çizgi roman okumuş ve şu bilgileri öğrenmişsin:

LEARNED KNOWLEDGE:
${learnedKnowledge}

TASK: Bu öğrendiğin comic book techniques'i kullanarak gelişmiş bir FRP senaryosu yaz.

REQUIREMENTS:
Theme: ${theme}
Difficulty: ${difficulty}
Format: FRP kampanya formatında (Sahne 1, Karar Noktası, Zar Atışı, Beceri Kontrolü, Sonuç, Boss, Multi-round Combat, Status Effects)

COMIC STORYTELLING TECHNIQUES'İ KULLAN:
- Visual dramatic moments
- Comic book pacing (setup → tension → climax)
- Character archetypes öğrendiğin türden
- Dialogue styles comic'lerden öğrendiklerin
- Action sequences cinematic olsun
- Plot twists ve cliffhangers ekle

FRP MEKANİKLERİNİ DETAYLANDIR:
- Her karar noktasında oyuncu seçimleri, zar atışı (örn. d20, d6), ve beceri/stat kontrolü (örn. Strength, Arcana, Persuasion) ekle
- Savaşlarda initiative (inisiyatif), round bazlı combat, birden fazla düşman, multi-round aksiyonlar ve status effects (ör. poison, stun, fear) kullan
- Her combat için: düşman statları, saldırı/defans, özel yetenekler, ve olası durum etkileri belirt
- Combat sırasında zar atışlarının sonuçlarını ve olası varyasyonları açıkla

OUTPUT FORMAT:
### CAMPAIGN X: [Title]
Sahne 1: [Title]
Karar Noktası: [Aksiyon seçimi, zar atışı, beceri kontrolü]
Seçimler: A) [action, dice roll, skill check] B) [action, dice roll, skill check] ...
Sonuç: A=[result] B=[result] ...

Combat: [Initiative order, round-by-round actions, status effects]

Sahne 2: ...

Boss: [Name] (HP:[x], ATK:[x], DEF:[x], Special Abilities, Status Effects)

DETAILED COMBAT SEQUENCE:
[Comic book style, round-by-round, initiative, dice rolls, status effects, multi-enemy combat]

Generate now using your comic book knowledge and advanced FRP mechanics!
`;
  }
}
