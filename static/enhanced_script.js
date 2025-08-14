// COMPLETE GAME SYSTEM - ALL FEATURES RESTORED
console.log("=== COMPLETE GAME SYSTEM LOADED ===");

// GLOBAL FUNCTION DECLARATIONS - CRITICAL FOR HTML ONCLICK ATTRIBUTES
window.switchTheme = function (theme) {
  console.log("✅ SWITCH THEME:", theme);

  // Update theme tabs
  document.querySelectorAll(".theme-tab").forEach((tab) => {
    tab.classList.remove("active");
  });
  document
    .querySelector(`[onclick="switchTheme('${theme}')"]`)
    .classList.add("active");

  // Update theme content
  document.querySelectorAll(".theme-content").forEach((content) => {
    content.style.display = "none";
  });
  document.getElementById(`${theme}-content`).style.display = "block";

  // Show/hide scenario categories
  document.querySelectorAll(".scenario-category").forEach((category) => {
    category.style.display = "none";
  });
  document.getElementById(theme + "-scenarios").style.display = "block";

  // Initialize NPCs for the selected theme
  if (npcSystem && npcSystem.initializeNPCs) {
    npcSystem.initializeNPCs(theme);
  }
};

window.selectRace = function (element, race) {
  console.log("✅ SELECT RACE:", race);

  // Get the parent theme content
  const themeContent = element.closest(".theme-content");

  // Remove selection from all race items in this theme only
  themeContent
    .querySelectorAll(".race-class-list:nth-child(1) .list-item")
    .forEach((item) => {
      item.classList.remove("selected");
    });

  element.classList.add("selected");

  // Update character panel
  updateCharacterPanel();
};

window.selectClass = function (element, className) {
  console.log("✅ SELECT CLASS:", className);

  // Get the parent theme content
  const themeContent = element.closest(".theme-content");

  // Remove selection from all class items in this theme only
  themeContent
    .querySelectorAll(".race-class-list:nth-child(2) .list-item")
    .forEach((item) => {
      item.classList.remove("selected");
    });

  element.classList.add("selected");

  // Update character panel
  updateCharacterPanel();
};

window.selectScenario = function (scenarioId) {
  console.log("✅ SELECT SCENARIO:", scenarioId);

  const scenarioSelection = document.getElementById("scenario-selection");
  const activeGame = document.getElementById("active-game");

  if (scenarioSelection && activeGame) {
    scenarioSelection.style.display = "none";
    activeGame.style.display = "block";
    startScenario(scenarioId);
  }
};

window.generateAIScenario = function () {
  console.log("✅ GENERATE AI SCENARIO");
  const theme = document.getElementById("ai-theme").value;
  const difficulty = document.getElementById("ai-difficulty").value;
  const level = document.getElementById("ai-level").value;

  const generateBtn = document.querySelector(".generate-btn");
  const originalText = generateBtn.textContent;
  generateBtn.textContent = "🔄 Üretiliyor...";
  generateBtn.disabled = true;

  setTimeout(() => {
    const scenarioTitle = `${
      theme.charAt(0).toUpperCase() + theme.slice(1)
    } AI Senaryosu`;
    const scenarioDescription = `${difficulty} zorlukta, seviye ${level} için özel olarak üretilen AI destekli senaryo.`;

    const scenarioCard = document.createElement("div");
    scenarioCard.className = "scenario-card ai-generated";
    scenarioCard.innerHTML = `
      <div class="scenario-header">
        <h4>🤖 ${scenarioTitle}</h4>
        <span class="difficulty ${difficulty}">${difficulty}</span>
      </div>
      <p>${scenarioDescription}</p>
      <div class="ai-info">
        <small>AI tarafından üretildi • Seviye: ${level}</small>
      </div>
    `;

    const scenarioGrid = document.querySelector(".scenario-grid");
    if (scenarioGrid) {
      scenarioGrid.appendChild(scenarioCard);
    }

    generateBtn.textContent = originalText;
    generateBtn.disabled = false;
    console.log("✅ AI Scenario generated:", { theme, difficulty, level });
    alert("🤖 AI Senaryo başarıyla üretildi!");
  }, 2000);
};

// SCENARIOS DATABASE
const scenarios = {
  living_dragon_hunt: {
    id: "living_dragon_hunt",
    title: "🐉 Yaşayan Ejderha Avı",
    world: "Fantasy Dünyası",
    description: `Eldoria Krallığı'nın güneyindeki küçük köyümüz, son 50 yıldır barış içinde yaşıyordu. Ta ki o geceye kadar...

Kızıl Alev adındaki antik ejderha, dağların derinliklerinden çıkarak köyümüzü tehdit etmeye başladı. Her gece, köyün etrafında dolaşıyor, hayvanları kaçırıyor ve çiftçilerin tarlalarını yakıyor. Köylüler korku içinde evlerine kapanıyor, dualar ediyorlar.

Sen, bilinmeyen bir geçmişe sahip bir kahramansın. Köyün meydanında, hafızanı kaybetmiş halde bulundun. Yanında sadece eski bir kılıç ve üzerinde gizemli semboller olan bir kolye var. Köylüler seni "Ejderha Avcısı" olarak adlandırdılar.

Şimdi, hafızanı geri kazanmak ve köyü kurtarmak için tehlikeli bir yolculuğa çıkacaksın. Ejderha'nın gerçek amacını öğrenmek, köylülerin güvenini kazanmak ve belki de kendi geçmişini keşfetmek zorundasın.

Bu sadece bir ejderha avı değil - bu SENİN HİKAYEN. Her seçim seni değiştirecek, her karar dünyayı değiştirecek.`,
    objective: "Ejderhayı bul ve durdur - veya gerçeği keşfet",
    story: {
      start: {
        title: "Kendini Keşfet",
        text: "Gözlerini açtığında kendini yıkık bir köyde buluyorsun. Etrafında dumanlar tütüyor, insanlar panik içinde koşuşturuyor. Sen kimsin? Burada ne olmuş?",
        choices: [
          {
            text: "Kendini ve çevreni anlamaya çalış",
            nextNode: "self_discovery",
          },
          {
            text: "Yaralı bir köylüyü bul ve yardım et",
            nextNode: "help_villager",
          },
          {
            text: "Yıkıntıları incele ve izleri takip et",
            nextNode: "investigate_ruins",
          },
        ],
      },
      self_discovery: {
        title: "Kahraman Uyanışı",
        text: "Köyün kenarında duruyorsun. Belinde kılıcın, sırtında zırhın var. Sen bir savaşçısın ve bu köyü kurtarmak için buradasın.",
        choices: [
          {
            text: "Köylülerle konuş ve bilgi topla",
            nextNode: "gather_intelligence",
          },
          { text: "Silahlarını kontrol et", nextNode: "check_equipment" },
          { text: "Ejderha izlerini ara", nextNode: "track_dragon" },
        ],
      },

      gather_intelligence: {
        title: "Bilgi Toplama",
        text: "Köylülerle konuşuyorsun. Herkes farklı bir hikaye anlatıyor. Bazıları ejderhanın gece geldiğini, bazıları gündüz geldiğini söylüyor. Bir şeyler tuhaf...",
        choices: [
          { text: "Köyün yaşlısıyla konuş", nextNode: "talk_elder" },
          { text: "Çocuklardan bilgi al", nextNode: "question_children" },
          { text: "Köyün liderini bul", nextNode: "find_village_leader" },
        ],
      },

      talk_elder: {
        title: "Yaşlı Bilge",
        text: "Köyün yaşlısı sana garip bir hikaye anlatıyor: 'Ejderha yok, olamaz. Bu dağlarda yüzyıllardır ejderha görülmedi. Bu başka bir şey...'",
        choices: [
          { text: "Ne demek istiyorsun?", nextNode: "elder_revelation" },
          { text: "Eski efsaneleri anlat", nextNode: "ancient_legends" },
          { text: "Şüphelen ve sorgula", nextNode: "suspect_elder" },
        ],
      },

      elder_revelation: {
        title: "Yaşlı Bilgenin İtirafı",
        text: "Yaşlı gözlerini kısıyor: 'Bu bir tuzak. Seni buraya çekmek için kurulmuş bir plan. Ejderha yok, sadece seni öldürmek isteyenler var.'",
        choices: [
          { text: "Kim yapıyor bunu?", nextNode: "who_is_behind_it" },
          { text: "Neden beni öldürmek istiyorlar?", nextNode: "why_kill_me" },
          { text: "Yaşlıyı koru", nextNode: "protect_elder" },
        ],
      },

      who_is_behind_it: {
        title: "Arkasındaki Güç",
        text: "Yaşlı titreyen sesiyle: 'Kral... Kral seni istemiyor. Sen çok güçlüsün, tahtı için tehdit oluşturuyorsun. Bu köydeki herkes onun ajanı.'",
        choices: [
          { text: "Kralı öldürmeye git", nextNode: "go_kill_king" },
          { text: "Köyü yak", nextNode: "burn_treacherous_village" },
          { text: "Gizlice kaç", nextNode: "escape_secretly" },
        ],
      },

      go_kill_king: {
        title: "Krala Gidiş",
        text: "Kralın sarayına doğru yola çıkıyorsun. Artık gerçeği biliyorsun. Bu bir ejderha avı değil, bir suikast planı!",
        choices: [
          { text: "Saraya gizlice gir", nextNode: "sneak_into_palace" },
          { text: "Muhafızları öldür", nextNode: "kill_guards" },
          { text: "Kralı meydan oku", nextNode: "challenge_king" },
        ],
      },

      sneak_into_palace: {
        title: "Saraya Sızma",
        text: "Saraya gizlice sızdın. Karanlık koridorlarda ilerliyorsun. Kralın odasını bulmalısın.",
        choices: [
          { text: "Kralın odasını bul", nextNode: "find_kings_chamber" },
          { text: "Hazineden geç", nextNode: "pass_through_treasury" },
          { text: "Muhafızları atlat", nextNode: "avoid_guards" },
        ],
      },

      find_kings_chamber: {
        title: "Kralın Odası",
        text: "Kralın odasına ulaştın. Kral yatakta uyuyor. Şimdi ne yapacaksın?",
        choices: [
          { text: "Kralı uyandır", nextNode: "wake_king" },
          { text: "Sessizce öldür", nextNode: "silent_kill" },
          { text: "Kralı sorgula", nextNode: "interrogate_king" },
        ],
      },

      wake_king: {
        title: "Kral Uyandı",
        text: "Kralı uyandırdın. Gözlerini açıyor ve seni görüyor. 'Sen... sen hala hayattasın? Bu imkansız!'",
        choices: [
          {
            text: "Neden beni öldürmek istedin?",
            nextNode: "why_kill_me_king",
          },
          { text: "Tahtı bırak", nextNode: "demand_abdication" },
          { text: "Savaş", nextNode: "fight_king" },
        ],
      },

      why_kill_me_king: {
        title: "Kralın İtirafı",
        text: "Kral korkuyla: 'Sen... sen benim oğlumsun. Ama ben seni tanımadım. Sen bebekken kaybolmuştun. Şimdi geri döndün ve tahtı istiyorsun!'",
        choices: [
          { text: "Babam mı?", nextNode: "father_revelation" },
          { text: "Yalan söylüyorsun", nextNode: "call_king_liar" },
          { text: "Tahtı paylaş", nextNode: "share_throne" },
        ],
      },

      father_revelation: {
        title: "Baba Oğul",
        text: "Kral ağlıyor: 'Evet, sen benim oğlumsun. Seni kaybettiğimde çılgına döndüm. Şimdi geri döndün ama ben seni tanımadım ve öldürmeye çalıştım...'",
        choices: [
          { text: "Babamı affet", nextNode: "forgive_father" },
          { text: "Tahtı al", nextNode: "take_throne_from_father" },
          { text: "Birlikte yönet", nextNode: "rule_together" },
        ],
      },

      forgive_father: {
        title: "Affetme",
        text: "Babamı affettin. O da seni kucaklıyor. Artık birlikte krallığı yöneteceksiniz. Aile bağları güçlü.",
        choices: [
          { text: "Birlikte yönet", nextNode: "rule_with_father" },
          { text: "Babamı dinle", nextNode: "listen_to_father" },
          { text: "Aileyi koru", nextNode: "protect_family" },
        ],
      },

      rule_with_father: {
        title: "Birlikte Yönetim",
        text: "Babamla birlikte krallığı yönetiyorsun. O deneyimli, sen cesur. Mükemmel bir kombinasyon. Krallık refah içinde.",
        choices: [
          { text: "Krallığı büyüt", nextNode: "expand_kingdom" },
          { text: "Halkı koru", nextNode: "protect_people" },
          { text: "Aile mutluluğu", nextNode: "family_happiness" },
        ],
      },

      expand_kingdom: {
        title: "Krallığı Genişletme",
        text: "Krallığı genişletiyorsun. Yeni topraklar fethediyorsun, yeni halklar senin yönetimine giriyor. Güç artıyor.",
        choices: [
          { text: "Savaşla genişlet", nextNode: "expand_by_war" },
          { text: "Diplomasi ile genişlet", nextNode: "expand_by_diplomacy" },
          { text: "Ticaret ile genişlet", nextNode: "expand_by_trade" },
        ],
      },

      expand_by_war: {
        title: "Savaşla Genişleme",
        text: "Savaşla krallığı genişletiyorsun. Orduların güçlü, düşmanların zayıf. Zaferler kazanıyorsun.",
        choices: [
          { text: "Daha fazla savaş", nextNode: "more_war" },
          { text: "Barış yap", nextNode: "make_peace" },
          { text: "Fethedilen toprakları yönet", nextNode: "manage_conquered" },
        ],
      },

      more_war: {
        title: "Daha Fazla Savaş",
        text: "Daha fazla savaş yapıyorsun. Artık korkulan bir savaşçı oldun. Düşmanlar senden korkuyor.",
        choices: [
          { text: "Tüm dünyayı fethet", nextNode: "conquer_world" },
          { text: "Savaştan bık", nextNode: "tired_of_war" },
          { text: "Savaş tanrısı ol", nextNode: "become_war_god" },
        ],
      },

      conquer_world: {
        title: "Dünya Fatihi",
        text: "Tüm dünyayı fethettin! Artık sen dünya imparatorusun. Hiç kimse sana karşı duramıyor.",
        choices: [
          { text: "İmparatorluğu yönet", nextNode: "rule_empire" },
          { text: "Yeni düşmanlar ara", nextNode: "find_new_enemies" },
          { text: "Ölümsüzlük ara", nextNode: "seek_immortality" },
        ],
      },

      rule_empire: {
        title: "İmparatorluk Yönetimi",
        text: "Dünya imparatorluğunu yönetiyorsun. Milyonlarca insan senin yönetiminde. Güç mutlak.",
        choices: [
          { text: "Adil imparator ol", nextNode: "just_emperor" },
          { text: "Tiran imparator ol", nextNode: "tyrant_emperor" },
          { text: "İmparatorluğu böl", nextNode: "divide_empire" },
        ],
      },

      just_emperor: {
        title: "Adil İmparator",
        text: "Adil bir imparator oldun. Halk seni seviyor, dünya barış içinde. Sen iyi bir lider oldun.",
        choices: [
          { text: "Barışı sürdür", nextNode: "maintain_peace" },
          { text: "Demokrasi kur", nextNode: "establish_democracy" },
          { text: "Varis yetiştir", nextNode: "raise_heir" },
        ],
      },

      maintain_peace: {
        title: "Barışı Sürdürme",
        text: "Barışı sürdürüyorsun. Dünya refah içinde, halk mutlu. Sen tarihin en iyi imparatoru oldun.",
        choices: [
          { text: "Ebedi barış", nextNode: "eternal_peace" },
          { text: "Yeni keşifler", nextNode: "new_discoveries" },
          { text: "Uzay yolculuğu", nextNode: "space_travel" },
        ],
      },

      eternal_peace: {
        title: "Ebedi Barış",
        text: "Ebedi barışı sağladın. Dünya artık hiç savaş görmeyecek. Sen efsanevi bir lider oldun.",
        choices: [
          { text: "Efsanevi lider olarak yaşa", nextNode: "end" },
          { text: "Yeni dünyalar ara", nextNode: "end" },
          { text: "Ölümsüzlük kazan", nextNode: "end" },
        ],
      },
      help_villager: {
        title: "Gizli Ajan",
        text: "Yaralı bir yaşlı kadın buluyorsun. Ama bir şeyler tuhaf... Ellerinde nasırlar var, gözlerinde profesyonel bir bakış. Bu kadın gerçekten köylü mü?",
        choices: [
          {
            text: "Hikayesini dinle (dikkatli ol)",
            nextNode: "suspicious_story",
          },
          { text: "Yaralarını kontrol et", nextNode: "check_wounds" },
          { text: "Kimliğini sorgula", nextNode: "interrogate_villager" },
        ],
      },
      investigate_ruins: {
        title: "Dünyayı Anlamak",
        text: "Yıkıntıları inceliyorsun. Bu sadece bir oyun değil - gerçek bir yer, gerçek insanların yaşadığı bir dünya. Her iz, her parça bir hikaye anlatıyor.",
        choices: [
          { text: "İzleri dikkatlice incele", nextNode: "examine_clues" },
          { text: "Köyün geçmişini öğren", nextNode: "learn_history" },
          { text: "Ne olduğunu anlamaya çalış", nextNode: "understand_events" },
        ],
      },
      memory_recovery: {
        title: "Hafıza Geri Dönüşü",
        text: "Gözlerini kapatıp derin nefes alıyorsun. Anılar yavaş yavaş geri geliyor... Sen bu köyün bir parçasısın. Ejderha saldırısından önce burada yaşıyordun.",
        choices: [
          { text: "Ailenin nerede olduğunu ara", nextNode: "meet_villagers" },
          { text: "Köyün durumunu değerlendir", nextNode: "understand_world" },
          {
            text: "Diğer hayatta kalanlarla birleş",
            nextNode: "help_villager",
          },
        ],
      },
      meet_villagers: {
        title: "Köylüler mi?",
        text: "Köylüler sana şüpheyle bakıyor. Ama bir şeyler tuhaf... Bazılarının silahları var, bazıları çok iyi organize olmuş. Bu gerçekten bir köy mü yoksa başka bir şey mi?",
        choices: [
          {
            text: "Hikayelerini dinle (şüpheli)",
            nextNode: "villager_stories",
          },
          { text: "Silahlarını kontrol et", nextNode: "check_weapons" },
          {
            text: "Köyün gerçek amacını ara",
            nextNode: "investigate_village_purpose",
          },
        ],
      },
      understand_world: {
        title: "Dünyayı Anlamak",
        text: "Çevrene bakıyorsun. Bu dünya gerçek, bu insanlar gerçek. Sen de gerçeksin. Bu sadece bir oyun değil - bu senin hayatın.",
        choices: [
          { text: "Köyün geleceğini düşün", nextNode: "examine_clues" },
          { text: "Kendini bu dünyada konumlandır", nextNode: "learn_history" },
          { text: "Ne yapman gerektiğini anla", nextNode: "understand_events" },
        ],
      },
      listen_story: {
        title: "Yaşlı Kadının Hikayesi",
        text: "Yaşlı kadın titreyen sesiyle anlatıyor: 'Ejderha gece geldi. Ateş yağdırdı. Çocuklarımı kaybettim...' Gözlerinde yaşlar var.",
        choices: [
          { text: "Onu teselli et", nextNode: "gain_trust" },
          { text: "Ejderhayı durdurmaya söz ver", nextNode: "examine_clues" },
          { text: "Diğer kayıpları öğren", nextNode: "end" },
        ],
      },
      heal_wounds: {
        title: "Yaraları Tedavi",
        text: "Yaralarını tedavi ederken, bu sadece fiziksel değil. Onun ruhsal yaralarını da iyileştirmeye çalışıyorsun. Bu gerçek bir insan.",
        choices: [
          { text: "Tedaviyi tamamla", nextNode: "gain_trust" },
          { text: "Onun güvenini kazan", nextNode: "meet_villagers" },
          { text: "Diğer yaralılara yardım et", nextNode: "end" },
        ],
      },
      gain_trust: {
        title: "Güven Kazanma",
        text: "Yavaş yavaş güvenini kazanıyorsun. Seni artık bir yabancı değil, dost olarak görüyor. Bu bağ gerçek ve değerli.",
        choices: [
          { text: "Ejderhayı aramaya başla", nextNode: "dragon_hunt_begin" },
          {
            text: "Köyü savunmaya hazırla",
            nextNode: "prepare_village_defense",
          },
          { text: "Diğer kahramanları topla", nextNode: "gather_heroes" },
        ],
      },
      examine_clues: {
        title: "İzleri İnceleme",
        text: "Yıkıntıları dikkatlice inceliyorsun. Ejderhanın izleri, yanmış evler, korku dolu anılar. Her şey bir hikaye anlatıyor.",
        choices: [
          { text: "Ejderhanın mağarasını bul", nextNode: "find_dragon_cave" },
          {
            text: "Ejderhanın zayıf noktalarını ara",
            nextNode: "find_dragon_weakness",
          },
          { text: "Savaş planı yap", nextNode: "plan_dragon_battle" },
        ],
      },
      learn_history: {
        title: "Köyün Geçmişi",
        text: "Köyün yaşlıları sana geçmişi anlatıyor. Bu köy yüzyıllardır burada. Ejderhalar hiç gelmemişti. Bu ilk kez.",
        choices: [
          { text: "Eski efsaneleri dinle", nextNode: "dragon_hunt_begin" },
          {
            text: "Köyün güçlü yanlarını öğren",
            nextNode: "prepare_village_defense",
          },
          { text: "Geçmiş tehditleri araştır", nextNode: "gather_heroes" },
        ],
      },
      understand_events: {
        title: "Olayları Anlama",
        text: "Parmaklarını yıkıntıların üzerinde gezdiriyorsun. Bu sadece bir saldırı değil - bu bir değişim. Dünya artık aynı değil.",
        choices: [
          { text: "Değişimin boyutunu anla", nextNode: "understand_scale" },
          { text: "Geleceği tahmin et", nextNode: "dragon_hunt_begin" },
          {
            text: "Hazırlanma yolları ara",
            nextNode: "prepare_village_defense",
          },
        ],
      },
      understand_scale: {
        title: "Değişimin Boyutunu Anlama",
        text: "Değişimin boyutunu anlıyorsun. Bu sadece bir köy değil - bu bir dünya değişimi. Her şey farklı olacak.",
        choices: [
          {
            text: "Ejderhayla savaşmaya karar ver",
            nextNode: "dragon_hunt_begin",
          },
          { text: "Köyü yeniden inşa et", nextNode: "rebuild_village" },
          { text: "Yeni bir hayat başlat", nextNode: "start_new_life" },
        ],
      },

      dragon_hunt_begin: {
        title: "Ejderha Avı Başlıyor",
        text: "Ejderhanın mağarasına doğru yola çıkıyorsun. Yanında güvendiğin dostların var. Bu sadece bir görev değil - bu senin kaderin.",
        choices: [
          { text: "Mağaraya gir", nextNode: "enter_dragon_cave" },
          { text: "Önce hazırlık yap", nextNode: "prepare_for_battle" },
          { text: "Tuzak kur", nextNode: "set_trap" },
        ],
      },

      enter_dragon_cave: {
        title: "Ejderha Mağarası",
        text: "Mağaranın derinliklerinde ejderhanın nefesini duyabiliyorsun. Karanlıkta gözleri yanıp sönüyor. Bu an geldi.",
        choices: [
          { text: "Ejderhayla konuşmaya çalış", nextNode: "talk_to_dragon" },
          { text: "Saldırıya geç", nextNode: "attack_dragon" },
          { text: "Gizlice yaklaş", nextNode: "stealth_approach" },
        ],
      },

      attack_dragon: {
        title: "Ejderha Savaşı",
        text: "Ejderhayla savaş başladı! Ateş yağıyor, kılıçlar çarpışıyor. Bu sadece bir savaş değil - bu senin kahramanlık anın.",
        choices: [
          { text: "Kılıçla saldır", nextNode: "sword_attack" },
          { text: "Büyü kullan", nextNode: "use_magic" },
          { text: "Taktik değiştir", nextNode: "change_tactics" },
        ],
      },

      sword_attack: {
        title: "Kılıç Saldırısı",
        text: "Kılıcını ejderhanın kalbine doğrultuyorsun. Bu tek şansın. Ya kazanacaksın ya da öleceksin.",
        choices: [
          { text: "Son darbeyi vur", nextNode: "final_strike" },
          { text: "Savunmaya geç", nextNode: "defend_attack" },
          { text: "Kaç", nextNode: "escape_battle" },
        ],
      },

      final_strike: {
        title: "Son Darbe",
        text: "Kılıcını ejderhanın kalbine saplıyorsun! Ejderha son bir çığlık atıyor ve yere düşüyor. Sen kazandın!",
        choices: [
          { text: "Zaferi kutla", nextNode: "victory_celebration" },
          { text: "Köye dön", nextNode: "return_to_village" },
          { text: "Ejderhanın hazinesini al", nextNode: "claim_treasure" },
        ],
      },

      victory_celebration: {
        title: "Zafer Kutlaması",
        text: "Köyde büyük bir kutlama var. Seni kahraman olarak görüyorlar. Ejderhayı öldürdün ve köyü kurtardın!",
        choices: [
          { text: "Kahraman olarak kal", nextNode: "end" },
          { text: "Yeni maceralar ara", nextNode: "end" },
          { text: "Huzurlu bir hayat yaşa", nextNode: "end" },
        ],
      },

      prepare_village_defense: {
        title: "Köy Savunması",
        text: "Köyü savunmaya hazırlıyorsun. Barikatlar kuruyorsun, insanları organize ediyorsun. Ejderha geri dönerse hazır olacaksınız.",
        choices: [
          { text: "Barikatları güçlendir", nextNode: "strengthen_barricades" },
          { text: "Halkı eğit", nextNode: "train_villagers" },
          { text: "Sinyal sistemi kur", nextNode: "set_alarm_system" },
        ],
      },

      gather_heroes: {
        title: "Kahramanları Toplama",
        text: "Köydeki cesur insanları topluyorsun. Her biri farklı yeteneklere sahip. Birlikte ejderhayı durdurabilirsiniz.",
        choices: [
          { text: "Savaşçıları organize et", nextNode: "organize_warriors" },
          { text: "Büyücüleri topla", nextNode: "gather_mages" },
          { text: "Taktik planı yap", nextNode: "create_battle_plan" },
        ],
      },

      strengthen_barricades: {
        title: "Barikatları Güçlendirme",
        text: "Barikatları güçlendiriyorsun. Taşlar, ağaçlar, ne varsa kullanıyorsun. Köy artık daha güvenli.",
        choices: [
          { text: "Ejderha gelirse savaş", nextNode: "dragon_returns_battle" },
          { text: "Daha fazla hazırlık yap", nextNode: "more_preparation" },
          { text: "Gözcü nöbeti kur", nextNode: "set_watch" },
        ],
      },

      dragon_returns_battle: {
        title: "Ejderha Geri Döndü",
        text: "Ejderha geri döndü! Ama bu sefer hazırlıklısınız. Barikatlarınız sağlam, insanlarınız cesur.",
        choices: [
          { text: "Barikatlardan savaş", nextNode: "fight_from_barricades" },
          { text: "Yakın dövüşe çık", nextNode: "close_combat" },
          { text: "Tuzak kullan", nextNode: "use_traps" },
        ],
      },

      fight_from_barricades: {
        title: "Barikatlardan Savaş",
        text: "Barikatlarınızdan ejderhaya ok atıyorsunuz. Ejderha öfkeyle saldırıyor ama barikatlar sağlam.",
        choices: [
          { text: "Okları hedefle", nextNode: "aim_arrows" },
          { text: "Sıcak yağ dök", nextNode: "pour_hot_oil" },
          { text: "Son saldırıya geç", nextNode: "final_barricade_attack" },
        ],
      },

      final_barricade_attack: {
        title: "Son Barikat Saldırısı",
        text: "Son bir saldırı daha! Tüm gücünüzle ejderhaya saldırıyorsunuz. Ejderha yaralanıyor ve kaçıyor!",
        choices: [
          { text: "Takip et", nextNode: "chase_dragon" },
          { text: "Köyü koru", nextNode: "protect_village" },
          { text: "Yaralıları tedavi et", nextNode: "heal_wounded" },
        ],
      },

      chase_dragon: {
        title: "Ejderhayı Takip",
        text: "Yaralı ejderhayı takip ediyorsun. Mağarasına kadar gidiyorsun. Bu sefer onu tamamen durduracaksın.",
        choices: [
          { text: "Mağaraya gir", nextNode: "enter_dragon_cave" },
          { text: "Mağarayı kapat", nextNode: "seal_cave" },
          { text: "Yakıtla yak", nextNode: "burn_cave" },
        ],
      },

      suspicious_story: {
        title: "Şüpheli Hikaye",
        text: "Kadın hikayesini anlatıyor ama detaylar tutmuyor. Ejderha saldırısının zamanını karıştırıyor. Bu kadın yalan söylüyor!",
        choices: [
          { text: "Yalanını yakala", nextNode: "expose_lie" },
          { text: "Sessizce takip et", nextNode: "follow_secretly" },
          { text: "Güvenini kazanmaya çalış", nextNode: "gain_false_trust" },
        ],
      },

      expose_lie: {
        title: "Yalan Yakalandı",
        text: "Kadının yalanını yakaladın! Kadın bir bıçak çıkarıyor ve sana saldırıyor. Bu bir tuzak!",
        choices: [
          { text: "Savaş", nextNode: "fight_assassin" },
          { text: "Kaç", nextNode: "escape_assassin" },
          { text: "Konuşmaya çalış", nextNode: "negotiate_assassin" },
        ],
      },

      fight_assassin: {
        title: "Suikastçı Savaşı",
        text: "Kadın profesyonel bir suikastçı! Kılıçlar çarpışıyor, bıçaklar uçuşuyor. Bu sadece bir ejderha avı değil - bu bir komplo!",
        choices: [
          { text: "Kılıçla saldır", nextNode: "sword_vs_assassin" },
          { text: "Çevreyi kullan", nextNode: "use_environment" },
          { text: "Yardım çağır", nextNode: "call_for_help" },
        ],
      },

      sword_vs_assassin: {
        title: "Kılıç Düellosu",
        text: "Suikastçıyla kılıç düellosu! O çok hızlı ve tehlikeli. Ama sen de deneyimli bir savaşçısın.",
        choices: [
          { text: "Son darbeyi vur", nextNode: "kill_assassin" },
          { text: "Yarala ve sorgula", nextNode: "wound_and_interrogate" },
          { text: "Teslim olmasını iste", nextNode: "demand_surrender" },
        ],
      },

      wound_and_interrogate: {
        title: "Sorgulama",
        text: "Suikastçıyı yaraladın. Şimdi gerçeği öğreneceksin. 'Kim gönderdi seni? Bu köyün gerçek amacı ne?'",
        choices: [
          { text: "Zorla konuştur", nextNode: "force_confession" },
          { text: "Anlaşma teklif et", nextNode: "offer_deal" },
          { text: "Serbest bırak", nextNode: "release_assassin" },
        ],
      },

      force_confession: {
        title: "Zorla İtiraf",
        text: "Suikastçı itiraf ediyor: 'Bu köy bir tuzak! Ejderha yok, sadece seni öldürmek için kurulmuş bir plan var. Kral seni istemiyor.'",
        choices: [
          { text: "Köye dön ve intikam al", nextNode: "return_for_revenge" },
          { text: "Kralı bul", nextNode: "find_king" },
          { text: "Planı boz", nextNode: "sabotage_plan" },
        ],
      },

      return_for_revenge: {
        title: "İntikam Zamanı",
        text: "Köye dönüyorsun. Artık herkesin gerçek yüzünü biliyorsun. Bu bir köy değil, bir suikast merkezi!",
        choices: [
          { text: "Hepsini öldür", nextNode: "kill_everyone" },
          { text: "Lideri bul", nextNode: "find_leader" },
          { text: "Köyü yak", nextNode: "burn_village" },
        ],
      },

      kill_everyone: {
        title: "Kanlı İntikam",
        text: "Köydeki herkesi öldürüyorsun. Kılıcın kanla kaplı. Artık sen korkulan bir savaşçısın. Karma: -100",
        choices: [
          { text: "Kralın sarayına git", nextNode: "go_to_palace" },
          { text: "Kaçak olarak yaşa", nextNode: "live_as_fugitive" },
          { text: "Yeni bir hayat başlat", nextNode: "start_new_life" },
        ],
      },

      go_to_palace: {
        title: "Saray Saldırısı",
        text: "Kralın sarayına gidiyorsun. Muhafızlar seni durdurmaya çalışıyor ama sen çok güçlüsün. Kral nerede?",
        choices: [
          { text: "Kralı bul ve öldür", nextNode: "kill_king" },
          { text: "Sarayı yak", nextNode: "burn_palace" },
          { text: "Kralı tahttan indir", nextNode: "dethrone_king" },
        ],
      },

      kill_king: {
        title: "Kral Katili",
        text: "Kralı öldürdün! Artık sen korkulan bir katilsin. Krallık kaosa düştü. Sen yeni kral olabilirsin...",
        choices: [
          { text: "Tahtı ele geçir", nextNode: "claim_throne" },
          { text: "Kaosu izle", nextNode: "watch_chaos" },
          { text: "Ülkeyi terk et", nextNode: "leave_country" },
        ],
      },

      claim_throne: {
        title: "Yeni Kral",
        text: "Tahtı ele geçirdin! Artık sen kralsın. Ama bu güç seni değiştiriyor. Korkulan bir tiran mı olacaksın?",
        choices: [
          { text: "Adil kral ol", nextNode: "just_king_ending" },
          { text: "Tiran ol", nextNode: "tyrant_ending" },
          { text: "Tahtı bırak", nextNode: "abandon_throne" },
        ],
      },

      just_king_ending: {
        title: "Adil Kral",
        text: "Krallığı adaletle yönetiyorsun. Halk seni seviyor, ülke refah içinde. Sen iyi bir kral oldun. Karma: +100",
        choices: [
          { text: "Krallığı sürdür", nextNode: "end" },
          { text: "Varis yetiştir", nextNode: "end" },
          { text: "Demokrasi kur", nextNode: "end" },
        ],
      },

      tyrant_ending: {
        title: "Korkunç Tiran",
        text: "Güç seni bozdu. Artık korkulan bir tiran oldun. Halk senden nefret ediyor ama korkuyor. Karma: -200",
        choices: [
          { text: "Zulmü sürdür", nextNode: "end" },
          { text: "İsyanı bastır", nextNode: "end" },
          { text: "Ölümü bekle", nextNode: "end" },
        ],
      },

      abandon_throne: {
        title: "Bilge Karar",
        text: "Tahtı bıraktın. Güç seni bozmadı. Artık özgür bir maceracısın. Halk seni saygıyla anıyor. Karma: +50",
        choices: [
          { text: "Yeni maceralar ara", nextNode: "end" },
          { text: "Barış içinde yaşa", nextNode: "end" },
          { text: "Öğretmen ol", nextNode: "end" },
        ],
      },

      live_as_fugitive: {
        title: "Kaçak Hayat",
        text: "Kaçak olarak yaşıyorsun. Her yerden aranıyorsun ama özgürsün. Bu zor bir hayat ama seni güçlendiriyor.",
        choices: [
          { text: "Yeraltı dünyasına gir", nextNode: "underground_life" },
          { text: "Yeni kimlik al", nextNode: "new_identity" },
          { text: "Sürgünde yaşa", nextNode: "exile_life" },
        ],
      },

      underground_life: {
        title: "Yeraltı Dünyası",
        text: "Yeraltı dünyasında yaşıyorsun. Hırsızlar, katiller, kaçaklar... Sen de onlardan birisin artık.",
        choices: [
          { text: "Çete lideri ol", nextNode: "gang_leader" },
          { text: "Tek başına yaşa", nextNode: "lone_wolf" },
          { text: "Yeraltı kralı ol", nextNode: "underground_king" },
        ],
      },

      gang_leader: {
        title: "Çete Lideri",
        text: "Yeraltı dünyasında kendi çeteni kurdun. Artık sen korkulan bir çete liderisin. Güç ve para senin.",
        choices: [
          { text: "Çeteyi büyüt", nextNode: "expand_gang" },
          { text: "Yasal işe geç", nextNode: "go_legitimate" },
          { text: "Rakip çetelerle savaş", nextNode: "gang_war" },
        ],
      },
      end: {
        title: "Başarılı Son",
        text: "Maceranı başarıyla tamamladın! Ejderhayı durdurdun ve köyü kurtardın. Bu sadece bir zafer değil, senin hikayenin bir parçası.",
        choices: [],
      },
    },
  },

  cyberpunk_hive_city: {
    id: "cyberpunk_hive_city",
    title: "🤖 Hive City Kriz",
    world: "Cyberpunk Dünyası",
    description: `2077 - Night City'nin en tehlikeli bölgesi Hive City'de karanlık bir savaş başlıyor...

Hive City, Night City'nin en alt katmanı. Burada yaşayanlar MegaCorp'ların zulmü altında eziliyor. Netrunner'lar, hacker'lar ve cyberpunk'lar burada gizleniyor. Son zamanlarda MegaCorp'lara karşı büyük bir isyan başladı. Netrunner'lar sistemleri hack ediyor, güvenlik duvarlarını aşıyor.

Sen, hafızanı kaybetmiş bir cyberpunk'sın. Vücudunda gelişmiş cyberware'ler var, neural link'in yanıp sönüyor. Yanında eski bir pistol ve gizemli bir data chip var. Hive City'nin sakinleri seni "Matrix'in Seçilmişi" olarak görüyor.

Şimdi, hafızanı geri kazanmak ve Hive City'nin kaderini belirlemek için tehlikeli bir yolculuğa çıkacaksın. MegaCorp'larla savaşmak, netrunner'ların güvenini kazanmak ve belki de kendi geçmişini keşfetmek zorundasın.

Bu sadece bir isyan değil - bu SENİN ŞEHRİN. Her seçim seni değiştirecek, her karar Night City'yi değiştirecek. "Wake up, samurai..."`,
    objective: "İsyanı yönet veya bastır - şehrin kaderini belirle",
    story: {
      start: {
        title: "Hive City'de Uyanış",
        text: "Hive City'nin alt katmanlarında gözlerini açıyorsun. Neon ışıklar yanıp sönüyor, cyberware'lerin ağrıyor. Şehirde bir isyan var.",
        choices: [
          { text: "Kendini bul", nextNode: "cyberpunk_self_discovery" },
          {
            text: "Yaralı bir netrunner'a yardım et",
            nextNode: "help_netrunner",
          },
          { text: "Şehri anlamaya çalış", nextNode: "understand_city" },
        ],
      },
      cyberpunk_self_discovery: {
        title: "Kendini Bul",
        text: "Hive City'nin alt katmanlarında kendini buluyorsun. Cyberware'lerin yanıp sönüyor, hafızan bulanık. Sen kimsin?",
        choices: [
          {
            text: "Hafızanı geri getirmeye çalış",
            nextNode: "understand_city",
          },
          { text: "Çevrendeki insanlarla konuş", nextNode: "help_netrunner" },
          { text: "Şehrin durumunu anla", nextNode: "work_corp" },
        ],
      },
      help_netrunner: {
        title: "Netrunner'a Yardım",
        text: "Yaralı bir netrunner buluyorsun. Gözlerinde korku ve umut var. Ona yardım ederken, bu sadece bir görev değil, gerçek bir insana yardım ettiğini hissediyorsun.",
        choices: [
          { text: "Onun hikayesini dinle", nextNode: "join_rebels" },
          { text: "Yaralarını tedavi et", nextNode: "work_corp" },
          { text: "Güvenini kazanmaya çalış", nextNode: "end" },
        ],
      },
      understand_city: {
        title: "Şehri Anlamak",
        text: "Şehrin sistemlerini inceliyorsun. Bu sadece bir oyun değil - gerçek bir şehir, gerçek insanların yaşadığı bir dünya.",
        choices: [
          { text: "Sistemleri dikkatlice incele", nextNode: "work_corp" },
          { text: "Şehrin geçmişini öğren", nextNode: "join_rebels" },
          { text: "Ne olduğunu anlamaya çalış", nextNode: "end" },
        ],
      },
      work_corp: {
        title: "MegaCorp Görevi",
        text: "MegaCorp'un güvenlik şefi size isyanı bastırma görevi veriyor. Netrunner'ları bulup durdurmak zorundasınız.",
        choices: [
          { text: "Netrunner'ları ara", nextNode: "end" },
          { text: "Sistemleri güçlendir", nextNode: "end" },
        ],
      },
      join_rebels: {
        title: "İsyancılar",
        text: "Netrunner'larla tanışıyorsun. Onlar MegaCorp'un zulmüne karşı savaşıyor. Sen de onlara katılabilirsin.",
        choices: [
          { text: "İsyana katıl", nextNode: "join_rebellion" },
          { text: "Planları öğren", nextNode: "learn_plans" },
        ],
      },
      end: {
        title: "Cyberpunk Sonu",
        text: "Hive City'deki maceran bitti. İsyanı çözdün veya katıldın. Bu sadece bir son değil, yeni bir başlangıç.",
        choices: [],
      },
    },
  },

  warhammer_imperial_crisis: {
    id: "warhammer_imperial_crisis",
    title: "💀 İmperium Krizi",
    world: "Warhammer 40K Dünyası",
    description: `M.41.999 - İmperium'un uzak sınır dünyası Cadia Prime'da karanlık bir tehdit büyüyor...

Cadia Prime, İmperium'un en önemli savunma dünyalarından biri. Cadian Shock Troops'ların efsanevi dünyası. Ancak son zamanlarda garip olaylar yaşanıyor. Köylüler gece gizlice toplanıyor, tuhaf semboller çiziliyor, dualar okunuyor. Chaos'un karanlık güçleri bu dünyaya sızıyor.

Sen, hafızanı kaybetmiş bir İmperium askerisin. Power armor'ının üzerinde Cadian Shock Troops'un sembolü var. Yanında lasgun'ın ve kutsal bir kolye var. Köylüler seni "İmperium'un Seçilmişi" olarak görüyor.

Şimdi, hafızanı geri kazanmak ve Cadia Prime'ı Chaos'tan korumak için tehlikeli bir göreve çıkacaksın. Chaos kültünü bulmak, köylülerin güvenini kazanmak ve belki de kendi geçmişini keşfetmek zorundasın.

Bu sadece bir savaş değil - bu SENİN DÜNYAN. Her seçim seni değiştirecek, her karar İmperium'u değiştirecek. "Ave Imperator!"`,
    objective: "Chaos kültünü bul ve yok et - İmperium'u koru",
    story: {
      start: {
        title: "İmperium'da Uyanış",
        text: "İmperium'un uzak bir dünyasında gözlerini açıyorsun. Power armor'ın ağırlığını hissediyorsun. Chaos tehdidi artıyor.",
        choices: [
          { text: "Kendini keşfet", nextNode: "warhammer_self_discovery" },
          { text: "Yaralı bir askere yardım et", nextNode: "help_soldier" },
          {
            text: "Dünyanın durumunu anla",
            nextNode: "understand_world_state",
          },
        ],
      },
      warhammer_self_discovery: {
        title: "Kendini Keşfet",
        text: "İmperium'un uzak bir dünyasında kendini buluyorsun. Power armor'ın ağırlığını hissediyorsun, hafızan bulanık. Sen kimsin?",
        choices: [
          { text: "Hafızanı geri getirmeye çalış", nextNode: "help_soldier" },
          {
            text: "Çevrendeki askerlerle konuş",
            nextNode: "investigate_village",
          },
          {
            text: "Dünyanın durumunu anla",
            nextNode: "understand_world_state",
          },
        ],
      },
      help_soldier: {
        title: "Asker'e Yardım",
        text: "Yaralı bir Imperial Guardsman buluyorsun. Gözlerinde korku ve sadakat var. Ona yardım ederken, bu sadece bir görev değil, gerçek bir askere yardım ettiğini hissediyorsun.",
        choices: [
          {
            text: "Onun hikayesini dinle",
            nextNode: "warhammer_self_discovery",
          },
          { text: "Yaralarını tedavi et", nextNode: "understand_world_state" },
          { text: "Güvenini kazanmaya çalış", nextNode: "investigate_village" },
        ],
      },
      understand_world_state: {
        title: "Dünyanın Durumunu Anlamak",
        text: "Dünyanın durumunu inceliyorsun. Bu sadece bir oyun değil - gerçek bir dünya, gerçek insanların yaşadığı bir yer.",
        choices: [
          {
            text: "Dünyayı dikkatlice incele",
            nextNode: "investigate_village",
          },
          { text: "Dünyanın geçmişini öğren", nextNode: "night_surveillance" },
          { text: "Ne olduğunu anlamaya çalış", nextNode: "end" },
        ],
      },
      investigate_village: {
        title: "Köy Araştırması",
        text: "Köyde garip olaylar yaşanıyor. İnsanlar gece gizlice toplanıyor, tuhaf semboller çiziliyor.",
        choices: [
          { text: "Gece gözlemi yap", nextNode: "night_surveillance" },
          {
            text: "Şüpheli kişileri sorgula",
            nextNode: "interrogate_suspects",
          },
        ],
      },
      night_surveillance: {
        title: "Gece Gözlemi",
        text: "Gece gizlice köyü gözlemliyorsun. İnsanlar garip ayinler yapıyor. Bu Chaos kültü olabilir.",
        choices: [
          { text: "Kültü araştır", nextNode: "investigate_cult" },
          { text: "Yetkililere bildir", nextNode: "report_authorities" },
        ],
      },

      investigate_cult: {
        title: "Kült Araştırması",
        text: "Kültü araştırıyorsun. İnsanlar garip semboller çiziyor, tuhaf dualar okuyor. Bu gerçekten Chaos kültü!",
        choices: [
          { text: "Kült liderini bul", nextNode: "find_cult_leader" },
          { text: "Kültü infiltre et", nextNode: "infiltrate_cult" },
          { text: "Kültü yok et", nextNode: "destroy_cult" },
        ],
      },

      find_cult_leader: {
        title: "Kült Liderini Bulma",
        text: "Kült liderini buldun. O çok güçlü bir Chaos büyücüsü. Seni görünce saldırıya geçiyor!",
        choices: [
          { text: "Savaş", nextNode: "fight_cult_leader" },
          { text: "Büyü kullan", nextNode: "use_magic_against_cult" },
          { text: "Yardım çağır", nextNode: "call_for_help_cult" },
        ],
      },

      fight_cult_leader: {
        title: "Kült Lideri Savaşı",
        text: "Kült lideriyle savaşıyorsun! O Chaos büyüleri kullanıyor, sen kılıcınla karşılık veriyorsun.",
        choices: [
          { text: "Kılıçla saldır", nextNode: "sword_attack_cult" },
          { text: "Zırhını kullan", nextNode: "use_armor_defense" },
          { text: "Taktik değiştir", nextNode: "change_tactics_cult" },
        ],
      },

      sword_attack_cult: {
        title: "Kılıç Saldırısı",
        text: "Kılıcınla kült liderine saldırıyorsun. O büyü kalkanı kullanıyor ama sen güçlüsün!",
        choices: [
          { text: "Son darbeyi vur", nextNode: "final_strike_cult" },
          { text: "Savunmaya geç", nextNode: "defend_attack_cult" },
          { text: "Kaç", nextNode: "escape_cult_fight" },
        ],
      },

      final_strike_cult: {
        title: "Son Darbe",
        text: "Son darbeyi vurdun! Kült lideri yere düşüyor. Chaos kültü dağılıyor. Sen kazandın!",
        choices: [
          { text: "Kültü tamamen yok et", nextNode: "completely_destroy_cult" },
          { text: "Esirleri kurtar", nextNode: "rescue_prisoners" },
          { text: "Yetkililere bildir", nextNode: "report_victory" },
        ],
      },

      completely_destroy_cult: {
        title: "Kültü Tamamen Yok Etme",
        text: "Kültü tamamen yok ettin. Tüm Chaos sembolleri yok edildi, kült üyeleri yakalandı. Köy güvende.",
        choices: [
          { text: "Zaferi kutla", nextNode: "celebrate_victory" },
          { text: "Köyü koru", nextNode: "protect_village_after" },
          { text: "Yeni görevler ara", nextNode: "seek_new_missions" },
        ],
      },

      report_authorities: {
        title: "Yetkililere Bildirme",
        text: "Yetkililere bildirdin. Imperial Guard geliyor. Onlarla birlikte kültü araştıracaksınız.",
        choices: [
          { text: "Guard ile araştır", nextNode: "investigate_with_guard" },
          { text: "Komutanla konuş", nextNode: "talk_commander" },
          { text: "Plan yap", nextNode: "make_plan_with_guard" },
        ],
      },

      investigate_with_guard: {
        title: "Guard ile Araştırma",
        text: "Imperial Guard ile birlikte kültü araştırıyorsun. Onlar profesyonel, sen cesur. Mükemmel ekip.",
        choices: [
          { text: "Kült üssünü bul", nextNode: "find_cult_base" },
          {
            text: "Şüpheli kişileri sorgula",
            nextNode: "interrogate_suspects",
          },
          { text: "Tuzak kur", nextNode: "set_trap_for_cult" },
        ],
      },

      find_cult_base: {
        title: "Kült Üssünü Bulma",
        text: "Kült üssünü buldun! Yeraltında büyük bir mağara. İçinde Chaos büyücüleri ve kült üyeleri var.",
        choices: [
          { text: "Saldırıya geç", nextNode: "attack_cult_base" },
          { text: "Gizlice gir", nextNode: "sneak_into_base" },
          { text: "Üssü kuşat", nextNode: "siege_cult_base" },
        ],
      },

      attack_cult_base: {
        title: "Kült Üssü Saldırısı",
        text: "Kült üssüne saldırıyorsun! Imperial Guard ile birlikte Chaos büyücülerine karşı savaşıyorsun.",
        choices: [
          { text: "Ön cephede savaş", nextNode: "front_line_battle" },
          { text: "Arka cephede destekle", nextNode: "support_from_rear" },
          { text: "Lideri hedefle", nextNode: "target_cult_leader" },
        ],
      },

      front_line_battle: {
        title: "Ön Cephe Savaşı",
        text: "Ön cephede savaşıyorsun! Chaos büyücüleri ateş yağdırıyor, sen kılıcınla karşılık veriyorsun.",
        choices: [
          { text: "Cesurca savaş", nextNode: "brave_battle" },
          { text: "Taktik kullan", nextNode: "use_tactics" },
          { text: "Yardım iste", nextNode: "request_help" },
        ],
      },

      brave_battle: {
        title: "Cesur Savaş",
        text: "Cesurca savaşıyorsun! Düşmanlar senden korkuyor. Imperial Guard seni takdir ediyor.",
        choices: [
          { text: "Zafer kazan", nextNode: "win_battle" },
          { text: "Düşmanı korkut", nextNode: "scare_enemy" },
          { text: "Kahraman ol", nextNode: "become_hero" },
        ],
      },

      win_battle: {
        title: "Savaşı Kazanma",
        text: "Savaşı kazandın! Chaos kültü tamamen yok edildi. Imperial Guard seni kahraman olarak görüyor.",
        choices: [
          { text: "Kahramanlık ödülü al", nextNode: "receive_hero_award" },
          { text: "Yeni görevler ara", nextNode: "seek_new_missions" },
          { text: "Barışı koru", nextNode: "maintain_peace" },
        ],
      },

      receive_hero_award: {
        title: "Kahramanlık Ödülü",
        text: "Kahramanlık ödülünü aldın! Imperial Guard seni onurlandırıyor. Artık sen korkulan bir savaşçısın.",
        choices: [
          { text: "Guard'a katıl", nextNode: "join_imperial_guard" },
          { text: "Bağımsız kal", nextNode: "stay_independent" },
          { text: "Yeni maceralar", nextNode: "new_adventures" },
        ],
      },

      join_imperial_guard: {
        title: "Imperial Guard'a Katılma",
        text: "Imperial Guard'a katıldın! Artık sen profesyonel bir askersin. İmperium için savaşacaksın.",
        choices: [
          { text: "Yüksel", nextNode: "rise_in_ranks" },
          { text: "Özel görevler al", nextNode: "special_missions" },
          { text: "Komutan ol", nextNode: "become_commander" },
        ],
      },

      rise_in_ranks: {
        title: "Rütbe Yükselme",
        text: "Rütben yükseliyor! Artık sen bir subaysın. Askerlerin sana saygı duyuyor.",
        choices: [
          { text: "Daha yüksek rütbe", nextNode: "higher_rank" },
          { text: "Özel birim kur", nextNode: "create_special_unit" },
          { text: "Savaş kahramanı ol", nextNode: "war_hero" },
        ],
      },

      war_hero: {
        title: "Savaş Kahramanı",
        text: "Savaş kahramanı oldun! İmperium'da ünlüsün. Herkes seni tanıyor ve saygı duyuyor.",
        choices: [
          { text: "Efsanevi kahraman ol", nextNode: "legendary_hero" },
          { text: "Öğretmen ol", nextNode: "become_teacher" },
          { text: "Emekli ol", nextNode: "retire_hero" },
        ],
      },

      legendary_hero: {
        title: "Efsanevi Kahraman",
        text: "Efsanevi kahraman oldun! İmperium'da efsane haline geldin. Seni herkes biliyor ve saygı duyuyor.",
        choices: [
          { text: "Efsanevi kahraman olarak yaşa", nextNode: "end" },
          { text: "Yeni nesiller yetiştir", nextNode: "end" },
          { text: "İmperium'u koru", nextNode: "end" },
        ],
      },

      // QUEST NODES
      blacksmith_quest: {
        title: "Demirci Görevi",
        text: "Demirci Thorin sana özel bir kılıç yapmak istiyor. Ama önce nadir bir metal bulman gerekiyor.",
        choices: [
          { text: "Nadir metali ara", nextNode: "search_rare_metal" },
          {
            text: "Başka bir silah iste",
            nextNode: "request_different_weapon",
          },
          { text: "Görevi reddet", nextNode: "refuse_blacksmith_quest" },
        ],
      },

      search_rare_metal: {
        title: "Nadir Metal Arama",
        text: "Nadir metali arıyorsun. Dağlarda, mağaralarda, eski kalıntılarda arayabilirsin.",
        choices: [
          { text: "Dağlarda ara", nextNode: "search_mountains" },
          { text: "Mağaralarda ara", nextNode: "search_caves" },
          { text: "Eski kalıntılarda ara", nextNode: "search_ruins" },
        ],
      },

      search_mountains: {
        title: "Dağlarda Arama",
        text: "Dağlarda nadir metali arıyorsun. Soğuk ve tehlikeli ama değerli şeyler bulabilirsin.",
        choices: [
          { text: "Yüksek zirvelere çık", nextNode: "climb_peaks" },
          { text: "Maden arayışı yap", nextNode: "search_mines" },
          { text: "Yaratıklarla savaş", nextNode: "fight_mountain_creatures" },
        ],
      },

      climb_peaks: {
        title: "Zirvelere Tırmanma",
        text: "Yüksek zirvelere tırmanıyorsun. Hava soğuk, rüzgar güçlü. Ama zirvede parlak bir metal görüyorsun!",
        choices: [
          { text: "Metali al", nextNode: "collect_metal" },
          { text: "Dikkatli incele", nextNode: "examine_metal_carefully" },
          { text: "Geri dön", nextNode: "return_from_peaks" },
        ],
      },

      collect_metal: {
        title: "Metal Toplama",
        text: "Nadir metali topladın! Bu çok değerli bir metal. Demirci Thorin çok memnun olacak.",
        choices: [
          { text: "Demirciye geri dön", nextNode: "return_to_blacksmith" },
          { text: "Daha fazla ara", nextNode: "search_more_metal" },
          { text: "Metali sat", nextNode: "sell_metal" },
        ],
      },

      return_to_blacksmith: {
        title: "Demirciye Dönüş",
        text: "Demirci Thorin'e nadir metali verdin. O çok memnun! Şimdi sana özel bir kılıç yapacak.",
        choices: [
          { text: "Kılıcı bekle", nextNode: "wait_for_sword" },
          { text: "Başka bir şey iste", nextNode: "request_other_item" },
          { text: "Ödül al", nextNode: "receive_blacksmith_reward" },
        ],
      },

      wait_for_sword: {
        title: "Kılıç Bekleme",
        text: "Demirci kılıcı yapıyor. Çekiç sesleri, kıvılcımlar... Sonunda kılıç hazır!",
        choices: [
          { text: "Kılıcı al", nextNode: "receive_sword" },
          { text: "Kılıcı test et", nextNode: "test_sword" },
          { text: "Kılıca isim ver", nextNode: "name_sword" },
        ],
      },

      receive_sword: {
        title: "Kılıç Alma",
        text: "Özel kılıcını aldın! Bu çok güçlü bir silah. Artık daha güçlü savaşabilirsin.",
        choices: [
          { text: "Kılıcı kullan", nextNode: "use_new_sword" },
          { text: "Kılıcı sergile", nextNode: "display_sword" },
          { text: "Yeni görevler ara", nextNode: "seek_new_quests" },
        ],
      },

      cyberpunk_hack: {
        title: "Cyberpunk Hack",
        text: "Netrunner Shadow sana büyük bir hack görevi veriyor. MegaCorp'un ana sistemine sızman gerekiyor.",
        choices: [
          { text: "Hack'i kabul et", nextNode: "accept_hack_mission" },
          { text: "Daha fazla bilgi iste", nextNode: "request_hack_info" },
          { text: "Görevi reddet", nextNode: "refuse_hack_mission" },
        ],
      },

      accept_hack_mission: {
        title: "Hack Görevini Kabul",
        text: "Hack görevini kabul ettin. MegaCorp'un ana sistemine sızmak tehlikeli ama ödüllü.",
        choices: [
          { text: "Sisteme sız", nextNode: "infiltrate_system" },
          { text: "Önce hazırlık yap", nextNode: "prepare_for_hack" },
          { text: "Yardımcı ara", nextNode: "find_hack_helper" },
        ],
      },

      infiltrate_system: {
        title: "Sisteme Sızma",
        text: "MegaCorp'un sistemine sızdın! Matrix'te ilerliyorsun. Güvenlik duvarları, AI'lar...",
        choices: [
          { text: "Veri çek", nextNode: "extract_data" },
          { text: "Sistemi boz", nextNode: "corrupt_system" },
          { text: "Gizlice ara", nextNode: "search_secretly" },
        ],
      },

      extract_data: {
        title: "Veri Çekme",
        text: "Veriyi çekiyorsun! MegaCorp'un gizli dosyalarını indiriyorsun. Bu çok değerli bilgi.",
        choices: [
          { text: "Veriyi Shadow'a ver", nextNode: "give_data_to_shadow" },
          { text: "Veriyi sat", nextNode: "sell_data" },
          { text: "Veriyi kullan", nextNode: "use_data" },
        ],
      },

      give_data_to_shadow: {
        title: "Veriyi Shadow'a Verme",
        text: "Veriyi Netrunner Shadow'a verdin. O çok memnun! Seni takdir ediyor ve ödül veriyor.",
        choices: [
          { text: "Ödülü al", nextNode: "receive_shadow_reward" },
          { text: "Yeni görev iste", nextNode: "request_new_mission" },
          { text: "Ortak ol", nextNode: "become_partner" },
        ],
      },

      commissar_quest: {
        title: "Komiser Görevi",
        text: "Komiser Kain sana düzen sağlamak için yardım istiyor. Köyde isyan çıkabilir.",
        choices: [
          { text: "Düzeni sağla", nextNode: "maintain_village_order" },
          { text: "İsyancıları bul", nextNode: "find_rebels" },
          { text: "Görevi reddet", nextNode: "refuse_commissar_quest" },
        ],
      },

      maintain_village_order: {
        title: "Köy Düzenini Sağlama",
        text: "Köyde düzeni sağlıyorsun. İnsanları organize ediyorsun, kuralları uyguluyorsun.",
        choices: [
          { text: "Sert ol", nextNode: "be_strict" },
          { text: "Adil ol", nextNode: "be_fair" },
          { text: "Yumuşak ol", nextNode: "be_gentle" },
        ],
      },

      be_strict: {
        title: "Sert Yönetim",
        text: "Sert bir yönetim uyguluyorsun. Kuralları katı uyguluyorsun. Düzen sağlanıyor ama halk korkuyor.",
        choices: [
          { text: "Sertliği sürdür", nextNode: "continue_strict" },
          { text: "Yumuşakla", nextNode: "soften_approach" },
          { text: "Ödül ver", nextNode: "give_rewards" },
        ],
      },

      continue_strict: {
        title: "Sertliği Sürdürme",
        text: "Sertliği sürdürüyorsun. Köy tamamen düzene girdi. Komiser Kain seni takdir ediyor.",
        choices: [
          { text: "Komiser ol", nextNode: "become_commissar" },
          { text: "Yeni görev al", nextNode: "get_new_commissar_mission" },
          { text: "Düzeni koru", nextNode: "maintain_order_permanently" },
        ],
      },

      become_commissar: {
        title: "Komiser Olma",
        text: "Komiser oldun! Artık sen de Imperial Guard'ın bir parçasısın. Düzen ve disiplin senin işin.",
        choices: [
          { text: "Yeni bölgeye git", nextNode: "go_to_new_area" },
          { text: "Eğitim ver", nextNode: "train_soldiers" },
          { text: "Yüksel", nextNode: "rise_in_commissar_ranks" },
        ],
      },

      psyker_quest: {
        title: "Psyker Görevi",
        text: "Psyker Zara sana psi güçlerini geliştirmek için yardım ediyor. Warp'ın gücünü öğreneceksin.",
        choices: [
          { text: "Psi güçlerini öğren", nextNode: "learn_psyker_powers" },
          { text: "Warp'ı keşfet", nextNode: "explore_warp" },
          { text: "Görevi reddet", nextNode: "refuse_psyker_quest" },
        ],
      },

      learn_psyker_powers: {
        title: "Psi Güçlerini Öğrenme",
        text: "Psi güçlerini öğreniyorsun. Zara sana Warp'ın sırlarını öğretiyor. Güç artıyor!",
        choices: [
          { text: "Telepati öğren", nextNode: "learn_telepathy" },
          { text: "Telekinezi öğren", nextNode: "learn_telekinesis" },
          { text: "Gelecek görü", nextNode: "learn_precognition" },
        ],
      },

      learn_telepathy: {
        title: "Telepati Öğrenme",
        text: "Telepati öğreniyorsun! Artık insanların düşüncelerini okuyabilirsin. Bu güçlü bir yetenek.",
        choices: [
          { text: "Gücü test et", nextNode: "test_telepathy" },
          { text: "Daha fazla öğren", nextNode: "learn_more_telepathy" },
          { text: "Gücü gizle", nextNode: "hide_telepathy" },
        ],
      },

      test_telepathy: {
        title: "Telepati Testi",
        text: "Telepati gücünü test ediyorsun. Köylülerin düşüncelerini okuyabiliyorsun. Bazıları şüpheli...",
        choices: [
          {
            text: "Şüpheli düşünceleri araştır",
            nextNode: "investigate_suspicious_thoughts",
          },
          { text: "Gücü kullanma", nextNode: "stop_using_telepathy" },
          { text: "Zara'ya bildir", nextNode: "report_to_zara" },
        ],
      },

      investigate_suspicious_thoughts: {
        title: "Şüpheli Düşünceleri Araştırma",
        text: "Şüpheli düşünceleri araştırıyorsun. Bazı köylüler Chaos hakkında düşünüyor!",
        choices: [
          { text: "Chaos kültünü araştır", nextNode: "investigate_cult" },
          { text: "Yetkililere bildir", nextNode: "report_authorities" },
          { text: "Gizlice takip et", nextNode: "secretly_follow" },
        ],
      },
      end: {
        title: "Warhammer Sonu",
        text: "İmperium krizini çözdün. Chaos tehdidini durdurdun. İmperium için savaştın ve kazandın.",
        choices: [],
      },
    },
  },
};

// GAME SYSTEMS
let playerKarma = 0;
let playerLevel = 1;
let playerExperience = 0;
let playerReputation = 0;

// NPC SYSTEM
const npcSystem = {
  npcs: {
    fantasy: {
      elder: {
        id: "elder",
        name: "Yaşlı Bilge",
        personality: "Bilge ve şüpheli",
        relationship: 0,
        quests: ["find_truth", "protect_village"],
        dialogue: {
          greeting: "Hoş geldin genç savaşçı. Burada ne arıyorsun?",
          quest: "Ejderha hakkında gerçeği öğrenmek ister misin?",
          farewell: "Dikkatli ol, her şey göründüğü gibi değil.",
        },
      },
      blacksmith: {
        id: "blacksmith",
        name: "Demirci Thorin",
        personality: "Güçlü ve güvenilir",
        relationship: 0,
        quests: ["forge_weapon", "repair_armor"],
        dialogue: {
          greeting: "Silahlarını kontrol etmek mi istiyorsun?",
          quest: "Yeni bir kılıç yapmamı ister misin?",
          farewell: "Silahların her zaman hazır olsun.",
        },
      },
      merchant: {
        id: "merchant",
        name: "Tüccar Alric",
        personality: "Açgözlü ama yardımcı",
        relationship: 0,
        quests: ["trade_goods", "find_treasure"],
        dialogue: {
          greeting: "En iyi mallar bende! Ne istiyorsun?",
          quest: "Hazine haritası var, ilgilenir misin?",
          farewell: "Tekrar gel, her zaman iyi fiyat veririm.",
        },
      },
    },
    cyberpunk: {
      netrunner: {
        id: "netrunner",
        name: "Netrunner Shadow",
        personality: "Gizemli ve tehlikeli",
        relationship: 0,
        quests: ["hack_system", "steal_data"],
        dialogue: {
          greeting: "Matrix'e hoş geldin, runner.",
          quest: "Büyük bir hack yapmak ister misin?",
          farewell: "Güvenli kal, chummer.",
        },
      },
      fixer: {
        id: "fixer",
        name: "Fixer Johnny",
        personality: "Bağlantılı ve güvenilir",
        relationship: 0,
        quests: ["get_job", "find_info"],
        dialogue: {
          greeting: "Ne iş var, choomba?",
          quest: "Büyük bir iş var, ilgilenir misin?",
          farewell: "İyi şanslar, edgerunner.",
        },
      },
      ripperdoc: {
        id: "ripperdoc",
        name: "Ripperdoc Chrome",
        personality: "Deli ama yetenekli",
        relationship: 0,
        quests: ["install_cyberware", "upgrade_body"],
        dialogue: {
          greeting: "Vücudunu geliştirmek mi istiyorsun?",
          quest: "Yeni cyberware var, denemek ister misin?",
          farewell: "Vücudun senin, istediğin gibi kullan.",
        },
      },
    },
    warhammer: {
      commissar: {
        id: "commissar",
        name: "Komiser Kain",
        personality: "Sert ve disiplinli",
        relationship: 0,
        quests: ["maintain_order", "punish_heretics"],
        dialogue: {
          greeting: "Dikkat, asker! Rapor ver!",
          quest: "Düzen sağlamak için yardım et!",
          farewell: "İmperium için savaş, asker!",
        },
      },
      techpriest: {
        id: "techpriest",
        name: "Tech-Priest Magos",
        personality: "Mekanik ve gizemli",
        relationship: 0,
        quests: ["repair_machine", "worship_omnissiah"],
        dialogue: {
          greeting: "Omnissiah'ın hizmetindeyim.",
          quest: "Makine ruhunu onarmak ister misin?",
          farewell: "Makine tanrısı seni korusun.",
        },
      },
      psyker: {
        id: "psyker",
        name: "Psyker Zara",
        personality: "Güçlü ama tehlikeli",
        relationship: 0,
        quests: ["use_powers", "control_warp"],
        dialogue: {
          greeting: "Warp'ın seslerini duyuyorum...",
          quest: "Psi güçlerini geliştirmek ister misin?",
          farewell: "Warp seni korusun.",
        },
      },
    },
  },

  initializeNPCs: function (theme) {
    console.log(`✅ Initializing NPCs for theme: ${theme}`);
    this.currentTheme = theme;
    this.updateNPCDisplay();
  },

  interactWithNPC: function (npcId) {
    const npc = this.npcs[this.currentTheme][npcId];
    if (!npc) return;

    npc.relationship += 10;
    this.showNPCDialogue(npc);
  },

  showNPCDialogue: function (npc) {
    const storyText = document.getElementById("story-text");
    const choicesGrid = document.getElementById("choices-grid");

    if (storyText && choicesGrid) {
      storyText.innerHTML = `
        <h3>${npc.name}</h3>
        <p><em>${npc.personality}</em></p>
        <p>${npc.dialogue.greeting}</p>
        <p><strong>İlişki:</strong> ${npc.relationship}</p>
      `;

      choicesGrid.innerHTML = `
        <button onclick="npcSystem.acceptQuest('${npc.id}', '${npc.quests[0]}')" class="choice-btn">
          Görev Al: ${npc.quests[0]}
        </button>
        <button onclick="npcSystem.talkToNPC('${npc.id}')" class="choice-btn">
          Konuş
        </button>
        <button onclick="npcSystem.returnToGame()" class="choice-btn">
          Geri Dön
        </button>
      `;
    }
  },

  acceptQuest: function (npcId, questId) {
    const npc = this.npcs[this.currentTheme][npcId];
    npc.relationship += 20;

    console.log(`✅ Quest accepted: ${questId} from ${npc.name}`);

    // Quest'e göre story node'a yönlendir
    this.startQuest(questId);
  },

  startQuest: function (questId) {
    const questNodes = {
      find_truth: "elder_revelation",
      protect_village: "prepare_village_defense",
      forge_weapon: "blacksmith_quest",
      hack_system: "cyberpunk_hack",
      maintain_order: "commissar_quest",
      use_powers: "psyker_quest",
    };

    const storyNode = questNodes[questId];
    if (storyNode) {
      loadStoryNode("living_dragon_hunt", storyNode);
    }
  },

  talkToNPC: function (npcId) {
    const npc = this.npcs[this.currentTheme][npcId];
    npc.relationship += 5;

    const storyText = document.getElementById("story-text");
    if (storyText) {
      storyText.innerHTML += `
        <p><strong>${npc.name}:</strong> ${npc.dialogue.quest}</p>
      `;
    }
  },

  returnToGame: function () {
    loadStoryNode("living_dragon_hunt", "self_discovery");
  },

  updateNPCDisplay: function () {
    const npcContainer = document.getElementById("npc-container");
    if (!npcContainer) return;

    const themeNPCs = this.npcs[this.currentTheme];
    npcContainer.innerHTML = "";

    Object.values(themeNPCs).forEach((npc) => {
      const npcElement = document.createElement("div");
      npcElement.className = "npc-item";
      npcElement.innerHTML = `
        <h4>${npc.name}</h4>
        <p>${npc.personality}</p>
        <p>İlişki: ${npc.relationship}</p>
        <button onclick="npcSystem.interactWithNPC('${npc.id}')" class="npc-interact-btn">
          Etkileşim
        </button>
      `;
      npcContainer.appendChild(npcElement);
    });
  },
};

// KARMA SYSTEM
function updateKarma(change) {
  playerKarma += change;
  console.log(`Karma updated: ${change} (Total: ${playerKarma})`);
  updateKarmaDisplay();
}

// LEVEL SYSTEM
function gainExperience(exp) {
  playerExperience += exp;
  const expNeeded = playerLevel * 100;

  if (playerExperience >= expNeeded) {
    playerLevel++;
    playerExperience -= expNeeded;
    console.log(`Level up! New level: ${playerLevel}`);
    updateLevelDisplay();
  }
}

// REPUTATION SYSTEM
function updateReputation(change) {
  playerReputation += change;
  console.log(`Reputation updated: ${change} (Total: ${playerReputation})`);
  updateReputationDisplay();
}

// DISPLAY UPDATES
function updateKarmaDisplay() {
  const karmaElement = document.getElementById("player-karma");
  if (karmaElement) {
    karmaElement.textContent = `Karma: ${playerKarma}`;
    karmaElement.className =
      playerKarma > 0
        ? "positive-karma"
        : playerKarma < 0
        ? "negative-karma"
        : "neutral-karma";
  }
}

function updateLevelDisplay() {
  const levelElement = document.getElementById("player-level");
  if (levelElement) {
    levelElement.textContent = `Level: ${playerLevel}`;
  }
}

function updateReputationDisplay() {
  const repElement = document.getElementById("player-reputation");
  if (repElement) {
    repElement.textContent = `Reputation: ${playerReputation}`;
  }
}

// GAME FUNCTIONS
function startScenario(scenarioId) {
  console.log("✅ STARTING SCENARIO:", scenarioId);

  const scenario = scenarios[scenarioId];
  if (!scenario) {
    console.error("❌ Scenario not found:", scenarioId);
    return;
  }

  // Reset player stats for new scenario
  playerKarma = 0;
  playerLevel = 1;
  playerExperience = 0;
  playerReputation = 0;

  showWorldBackstoryWithScenario(scenario);
}

function showWorldBackstoryWithScenario(scenario) {
  console.log("✅ SHOWING WORLD BACKSTORY");

  const currentScenarioTitle = document.getElementById(
    "current-scenario-title"
  );
  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (currentScenarioTitle && storyText && choicesGrid) {
    currentScenarioTitle.textContent = scenario.title;

    storyText.innerHTML = `
      <h3>${scenario.title}</h3>
      <p><strong>Dünya:</strong> ${scenario.world}</p>
      <p><strong>Açıklama:</strong> ${scenario.description}</p>
      <p><strong>Hedef:</strong> ${scenario.objective}</p>
    `;

    choicesGrid.innerHTML = `
      <button onclick="loadStoryNode('${scenario.id}', 'start')" class="choice-btn">
        Maceraya Başla
      </button>
    `;
  }
}

function loadStoryNode(scenarioId, nodeId) {
  console.log("✅ LOADING STORY NODE:", scenarioId, nodeId);

  const scenario = scenarios[scenarioId];
  if (!scenario || !scenario.story[nodeId]) {
    console.error("❌ Story node not found:", scenarioId, nodeId);
    return;
  }

  const node = scenario.story[nodeId];
  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (storyText && choicesGrid) {
    storyText.innerHTML = `
      <h3>${node.title}</h3>
      <p>${node.text}</p>
    `;

    if (node.choices && node.choices.length > 0) {
      choicesGrid.innerHTML = node.choices
        .map(
          (choice) => `
          <button onclick="loadStoryNode('${scenarioId}', '${choice.nextNode}')" class="choice-btn">
            ${choice.text}
          </button>
        `
        )
        .join("");
    } else {
      choicesGrid.innerHTML = `
        <button onclick="returnToScenarioSelection()" class="choice-btn">
          Senaryo Seçimine Dön
        </button>
      `;
    }
  }
}

function returnToScenarioSelection() {
  console.log("✅ RETURNING TO SCENARIO SELECTION");

  const scenarioSelection = document.getElementById("scenario-selection");
  const activeGame = document.getElementById("active-game");

  if (scenarioSelection && activeGame) {
    scenarioSelection.style.display = "block";
    activeGame.style.display = "none";
  }
}

// CHARACTER SYSTEM
window.updateCharacterName = function (name) {
  console.log("✅ UPDATE NAME:", name);
  const charNameElement = document.getElementById("char-name");
  if (charNameElement) {
    charNameElement.textContent = name;
  }
};

window.updateCharacterPanel = function () {
  console.log("✅ UPDATE CHARACTER PANEL");

  // Get selected race and class from the currently visible theme content
  const activeThemeContent = document.querySelector(
    ".theme-content[style*='block'], .theme-content:not([style*='none'])"
  );

  if (!activeThemeContent) {
    console.log("❌ No active theme content found");
    return;
  }

  // Get race and class lists from the active theme
  const raceClassLists =
    activeThemeContent.querySelectorAll(".race-class-list");

  let race = "Seçilmedi";
  let className = "Seçilmedi";

  // First list is races, second list is classes
  if (raceClassLists.length >= 2) {
    const raceList = raceClassLists[0];
    const classList = raceClassLists[1];

    const selectedRaceElement = raceList.querySelector(".list-item.selected");
    const selectedClassElement = classList.querySelector(".list-item.selected");

    if (selectedRaceElement) {
      race = selectedRaceElement.textContent.trim();
    }
    if (selectedClassElement) {
      className = selectedClassElement.textContent.trim();
    }
  }

  console.log("Selected Race:", race);
  console.log("Selected Class:", className);

  // Update character display
  const charNameElement = document.getElementById("char-name");
  const charRaceClassElement = document.getElementById("char-race-class");

  if (charNameElement && charRaceClassElement) {
    charRaceClassElement.textContent = `${race} • ${className}`;
  }
};

// FILE UPLOAD SYSTEM
function initializeFileUpload() {
  const fileInput = document.getElementById("file-input");
  const fileStatus = document.getElementById("file-status");
  const filesList = document.getElementById("files-list");

  if (fileInput) {
    fileInput.addEventListener("change", function (event) {
      const files = event.target.files;
      if (files.length > 0) {
        const file = files[0];
        fileStatus.textContent = `Seçilen dosya: ${file.name}`;

        const fileItem = document.createElement("div");
        fileItem.className = "file-item";
        fileItem.innerHTML = `
          <span>📄 ${file.name}</span>
          <span class="file-size">(${(file.size / 1024).toFixed(1)} KB)</span>
        `;
        filesList.appendChild(fileItem);
        console.log("✅ File uploaded:", file.name);
      }
    });
  }
}

// INITIALIZATION
document.addEventListener("DOMContentLoaded", function () {
  console.log("=== GAME ENHANCED HTML LOADED ===");
  console.log("JavaScript is working!");

  // Initialize file upload
  initializeFileUpload();

  // Check if all required elements exist
  const requiredElements = [
    "scenario-selection",
    "active-game",
    "current-scenario-title",
    "story-text",
    "choices-grid",
  ];

  console.log("DOM loaded, checking elements...");
  requiredElements.forEach((elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
      console.log(`✅ ${elementId}: Found`);
    } else {
      console.log(`❌ ${elementId}: Not found`);
    }
  });

  // Set default theme
  if (typeof switchTheme === "function") {
    switchTheme("fantasy");
  }
});

// ADDITIONAL STORY NODES - COMPLETING THE STORIES

// Fantasy Story Completion Nodes
scenarios.living_dragon_hunt.story.conquer_world = {
  title: "Dünya Fatihi",
  text: "Tüm dünyayı fethettin! Artık sen dünya imparatorusun. Krallığın tüm kıtalara yayıldı.",
  choices: [
    { text: "İmparatorluğu yönet", nextNode: "rule_empire" },
    { text: "Demokrasi kur", nextNode: "establish_democracy" },
    { text: "Tahtı bırak", nextNode: "leave_empire" },
  ],
};

scenarios.living_dragon_hunt.story.rule_empire = {
  title: "İmparatorluğu Yönetme",
  text: "İmparatorluğunu yönetiyorsun. Nasıl bir hükümdar olacaksın?",
  choices: [
    { text: "Adil imparator", nextNode: "just_emperor" },
    { text: "Tiran", nextNode: "tyrant_emperor" },
    { text: "Barışçı", nextNode: "peaceful_emperor" },
  ],
};

scenarios.living_dragon_hunt.story.just_emperor = {
  title: "Adil İmparator",
  text: "Adil bir imparator oldun. Halkın seni seviyor ve saygı duyuyor. İmparatorluğun altın çağını yaşıyor.",
  choices: [
    { text: "Barışı sürdür", nextNode: "maintain_peace" },
    { text: "Yeni keşifler", nextNode: "new_discoveries" },
    { text: "Vasiyet yaz", nextNode: "write_will" },
  ],
};

scenarios.living_dragon_hunt.story.maintain_peace = {
  title: "Barışı Sürdürme",
  text: "Barışı sürdürdün. İmparatorluğun ebedi barış içinde yaşıyor. Sen efsanevi bir hükümdar oldun.",
  choices: [
    { text: "Ebedi barış", nextNode: "eternal_peace" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

scenarios.living_dragon_hunt.story.eternal_peace = {
  title: "Ebedi Barış",
  text: "İmparatorluğun ebedi barış içinde yaşıyor. Sen tarihin en büyük hükümdarı oldun. Hikayen burada biter.",
  choices: [],
};

scenarios.living_dragon_hunt.story.tyrant_emperor = {
  title: "Tiran İmparator",
  text: "Tiran bir imparator oldun. Halk senden korkuyor ama güçlü bir imparatorluk kurdun.",
  choices: [
    { text: "Daha fazla baskı", nextNode: "more_oppression" },
    { text: "Yumuşat", nextNode: "soften_rule" },
    { text: "Devam et", nextNode: "continue_tyranny" },
  ],
};

scenarios.living_dragon_hunt.story.more_oppression = {
  title: "Daha Fazla Baskı",
  text: "Daha fazla baskı uyguluyorsun. İsyanlar başlıyor ama sen güçlüsün.",
  choices: [
    { text: "İsyanları bastır", nextNode: "crush_rebellions" },
    { text: "Daha da sert ol", nextNode: "become_crueler" },
    { text: "Dur", nextNode: "stop_oppression" },
  ],
};

scenarios.living_dragon_hunt.story.crush_rebellions = {
  title: "İsyanları Bastırma",
  text: "İsyanları bastırdın. Artık kimse sana karşı çıkmaya cesaret edemiyor.",
  choices: [
    { text: "Mutlak güç", nextNode: "absolute_power" },
    { text: "Korku imparatorluğu", nextNode: "empire_of_fear" },
    { text: "Son", nextNode: "tyrant_end" },
  ],
};

scenarios.living_dragon_hunt.story.absolute_power = {
  title: "Mutlak Güç",
  text: "Mutlak güce sahip oldun. Artık sen tanrı gibi güçlüsün. Hikayen burada biter.",
  choices: [],
};

// Warhammer Story Completion Nodes
scenarios.warhammer_imperial_crisis.story.report_authorities = {
  title: "Yetkililere Bildirme",
  text: "Chaos kültünü yetkililere bildirdin. İnquisitor geliyor.",
  choices: [
    { text: "İnquisitor ile çalış", nextNode: "work_with_inquisitor" },
    { text: "Kendi başına araştır", nextNode: "investigate_alone" },
    { text: "Bekle", nextNode: "wait_for_inquisitor" },
  ],
};

scenarios.warhammer_imperial_crisis.story.work_with_inquisitor = {
  title: "İnquisitor ile Çalışma",
  text: "İnquisitor ile birlikte çalışıyorsun. O çok güçlü ve deneyimli.",
  choices: [
    { text: "Kültü birlikte yok et", nextNode: "destroy_cult_together" },
    { text: "Daha fazla bilgi topla", nextNode: "gather_more_info" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.warhammer_imperial_crisis.story.destroy_cult_together = {
  title: "Kültü Birlikte Yok Etme",
  text: "İnquisitor ile birlikte Chaos kültünü yok ettin. İmperium güvende.",
  choices: [
    { text: "İmperium'a hizmet et", nextNode: "serve_imperium" },
    { text: "İnquisitor ol", nextNode: "become_inquisitor" },
    { text: "Normal hayata dön", nextNode: "return_to_normal" },
  ],
};

scenarios.warhammer_imperial_crisis.story.serve_imperium = {
  title: "İmperium'a Hizmet",
  text: "İmperium'a hizmet etmeye devam ediyorsun. Sen bir kahraman oldun.",
  choices: [
    { text: "Space Marine ol", nextNode: "become_space_marine" },
    { text: "Imperial Guard'da kal", nextNode: "stay_guard" },
    { text: "Commissar ol", nextNode: "become_commissar" },
  ],
};

scenarios.warhammer_imperial_crisis.story.become_space_marine = {
  title: "Space Marine Olma",
  text: "Space Marine oldun! Artık İmperium'un en güçlü savaşçılarından birisin.",
  choices: [
    { text: "Chapter'a katıl", nextNode: "join_chapter" },
    { text: "Savaşlara katıl", nextNode: "join_battles" },
    { text: "Eğitim al", nextNode: "receive_training" },
  ],
};

scenarios.warhammer_imperial_crisis.story.join_chapter = {
  title: "Chapter'a Katılma",
  text: "Ultramarines Chapter'ına katıldın. Artık efsanevi bir Space Marine'sin!",
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Savaş", nextNode: "fight_as_marine" },
    { text: "İmperium'u koru", nextNode: "protect_imperium" },
  ],
};

scenarios.warhammer_imperial_crisis.story.become_hero = {
  title: "Kahraman Olma",
  text: "İmperium'un en büyük kahramanlarından biri oldun. Hikayen burada biter.",
  choices: [],
};

// Cyberpunk Story Completion Nodes
scenarios.cyberpunk_hive_city.story.join_rebellion = {
  title: "İsyana Katılma",
  text: "Netrunner'lara katıldın. Artık MegaCorp'lara karşı savaşıyorsun.",
  choices: [
    { text: "Sistemleri hack et", nextNode: "hack_systems" },
    { text: "Saldırı planla", nextNode: "plan_attack" },
    { text: "Diğer isyancıları bul", nextNode: "find_rebels" },
  ],
};

scenarios.cyberpunk_hive_city.story.hack_systems = {
  title: "Sistemleri Hack Etme",
  text: "MegaCorp sistemlerini hack ettin. Güvenlik duvarlarını aştın.",
  choices: [
    { text: "Veri çal", nextNode: "steal_data" },
    { text: "Sistemleri boz", nextNode: "corrupt_systems" },
    { text: "Geri çekil", nextNode: "retreat_hack" },
  ],
};

scenarios.cyberpunk_hive_city.story.steal_data = {
  title: "Veri Çalma",
  text: "MegaCorp'un gizli verilerini çaldın. Artık onların tüm sırlarını biliyorsun.",
  choices: [
    { text: "Verileri yayınla", nextNode: "publish_data" },
    { text: "Şantaj yap", nextNode: "blackmail_corp" },
    { text: "Verileri sat", nextNode: "sell_data" },
  ],
};

scenarios.cyberpunk_hive_city.story.publish_data = {
  title: "Verileri Yayınlama",
  text: "MegaCorp'un tüm sırlarını yayınladın. Şehir karıştı, isyan büyüdü.",
  choices: [
    { text: "İsyanı yönet", nextNode: "lead_rebellion" },
    { text: "Kaç", nextNode: "escape_city" },
    { text: "Yeni hayat", nextNode: "new_life" },
  ],
};

scenarios.cyberpunk_hive_city.story.lead_rebellion = {
  title: "İsyanı Yönetme",
  text: "İsyanı yönetiyorsun. Artık sen Hive City'nin liderisin.",
  choices: [
    { text: "Şehri ele geçir", nextNode: "take_city" },
    { text: "MegaCorp'u yok et", nextNode: "destroy_corp" },
    { text: "Barış yap", nextNode: "make_peace_corp" },
  ],
};

scenarios.cyberpunk_hive_city.story.take_city = {
  title: "Şehri Ele Geçirme",
  text: "Hive City'yi ele geçirdin! Artık sen şehrin kralısın.",
  choices: [
    { text: "Şehri yönet", nextNode: "rule_city" },
    { text: "Yeni düzen kur", nextNode: "establish_new_order" },
    { text: "Özgürlük ver", nextNode: "give_freedom" },
  ],
};

scenarios.cyberpunk_hive_city.story.rule_city = {
  title: "Şehri Yönetme",
  text: "Hive City'yi yönetiyorsun. Artık sen Night City'nin en güçlü kişisisin.",
  choices: [
    { text: "Güçlü lider", nextNode: "powerful_leader" },
    { text: "Halkın lideri", nextNode: "peoples_leader" },
    { text: "Teknoloji kralı", nextNode: "tech_king" },
  ],
};

scenarios.cyberpunk_hive_city.story.powerful_leader = {
  title: "Güçlü Lider",
  text: "Night City'nin en güçlü lideri oldun. Hikayen burada biter.",
  choices: [],
};

// FANTASY MISSING NODES
scenarios.living_dragon_hunt.story.track_dragon = {
  title: "Ejderha İzlerini Takip",
  text: "Ejderha izlerini takip ediyorsun. Büyük pençe izleri, yanmış ağaçlar, korkmuş hayvanlar. Ejderha buradan geçmiş.",
  choices: [
    { text: "İzleri takip et", nextNode: "follow_tracks" },
    { text: "Ejderhanın yönünü tahmin et", nextNode: "predict_direction" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.follow_tracks = {
  title: "İzleri Takip Etme",
  text: "Ejderha izlerini takip ediyorsun. Dağlara doğru gidiyor. İzler giderek daha taze oluyor.",
  choices: [
    { text: "Mağaraya git", nextNode: "enter_dragon_cave" },
    { text: "Dikkatli ol", nextNode: "be_careful" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.enter_dragon_cave = {
  title: "Ejderha Mağarasına Giriş",
  text: "Ejderha mağarasına girdin. Karanlık ve sıcak. Ejderha burada!",
  choices: [
    { text: "Ejderhaya saldır", nextNode: "attack_dragon" },
    { text: "Gizlice yaklaş", nextNode: "sneak_to_dragon" },
    { text: "Kaç", nextNode: "escape_cave" },
  ],
};

scenarios.living_dragon_hunt.story.attack_dragon = {
  title: "Ejderhaya Saldırı",
  text: "Ejderhaya saldırdın! Kızıl Alev gözlerini açıyor ve sana bakıyor. Savaş başlıyor!",
  choices: [
    { text: "Kılıçla saldır", nextNode: "sword_attack" },
    { text: "Büyü kullan", nextNode: "use_magic" },
    { text: "Kaç", nextNode: "escape_battle" },
  ],
};

scenarios.living_dragon_hunt.story.sword_attack = {
  title: "Kılıç Saldırısı",
  text: "Kılıcınla ejderhaya saldırdın! Ejderha yaralandı ama hala güçlü.",
  choices: [
    { text: "Son darbeyi vur", nextNode: "final_strike" },
    { text: "Savunmaya geç", nextNode: "defend_attack" },
    { text: "Yardım çağır", nextNode: "call_for_help" },
  ],
};

scenarios.living_dragon_hunt.story.final_strike = {
  title: "Son Darbe",
  text: "Son darbeyi vurdun! Ejderha yere düştü. Zafer kazandın!",
  choices: [
    { text: "Zaferi kutla", nextNode: "victory_celebration" },
    { text: "Ejderhayı öldür", nextNode: "kill_dragon" },
    { text: "Ejderhayı serbest bırak", nextNode: "free_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.victory_celebration = {
  title: "Zafer Kutlaması",
  text: "Köye döndün. Herkes seni kahraman olarak karşılıyor. Ejderhayı yendin!",
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Köyü koru", nextNode: "protect_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.become_hero = {
  title: "Kahraman Olma",
  text: "Artık sen efsanevi bir kahramansın. Hikayen burada biter.",
  choices: [],
};

scenarios.living_dragon_hunt.story.check_equipment = {
  title: "Silahları Kontrol Etme",
  text: "Silahlarını kontrol ediyorsun. Kılıcın keskin, zırhın sağlam. Hazırsın.",
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Silahları geliştir", nextNode: "upgrade_weapons" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.prepare_for_battle = {
  title: "Savaşa Hazırlanma",
  text: "Savaşa hazırlanıyorsun. Silahların hazır, cesaretin tam.",
  choices: [
    { text: "Ejderhayı ara", nextNode: "search_for_dragon" },
    { text: "Köyü koru", nextNode: "defend_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.search_for_dragon = {
  title: "Ejderhayı Arama",
  text: "Ejderhayı arıyorsun. Dağlarda, ormanlarda iz sürüyorsun.",
  choices: [
    { text: "İzleri takip et", nextNode: "follow_tracks" },
    { text: "Gökyüzünü izle", nextNode: "watch_sky" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.question_children = {
  title: "Çocuklardan Bilgi Alma",
  text: "Çocuklarla konuşuyorsun. Onlar ejderhayı gördüklerini söylüyor.",
  choices: [
    { text: "Detayları öğren", nextNode: "learn_details" },
    { text: "Çocukları koru", nextNode: "protect_children" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.learn_details = {
  title: "Detayları Öğrenme",
  text: "Çocuklardan ejderha hakkında detaylı bilgi aldın. Büyük, kırmızı, ateş püskürüyor.",
  choices: [
    { text: "Ejderhayı ara", nextNode: "search_for_dragon" },
    { text: "Köyü uyar", nextNode: "warn_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.find_village_leader = {
  title: "Köy Liderini Bulma",
  text: "Köy liderini buldun. O çok endişeli ve sana yardım etmek istiyor.",
  choices: [
    { text: "Liderle konuş", nextNode: "talk_leader" },
    { text: "Yardım iste", nextNode: "ask_for_help" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.talk_leader = {
  title: "Liderle Konuşma",
  text: "Köy lideriyle konuşuyorsun. O ejderha hakkında çok şey biliyor.",
  choices: [
    { text: "Bilgi al", nextNode: "get_information" },
    { text: "Yardım iste", nextNode: "ask_for_help" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.get_information = {
  title: "Bilgi Alma",
  text: "Liderden ejderha hakkında çok bilgi aldın. Artık ne yapacağını biliyorsun.",
  choices: [
    { text: "Ejderhayı ara", nextNode: "search_for_dragon" },
    { text: "Köyü koru", nextNode: "defend_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.ancient_legends = {
  title: "Eski Efsaneler",
  text: "Yaşlı sana eski efsaneleri anlatıyor. Ejderha hakkında çok şey öğrendin.",
  choices: [
    { text: "Efsaneleri dinle", nextNode: "listen_legends" },
    { text: "Soru sor", nextNode: "ask_questions" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.listen_legends = {
  title: "Efsaneleri Dinleme",
  text: "Efsaneleri dinliyorsun. Ejderha hakkında çok şey öğrendin.",
  choices: [
    { text: "Ejderhayı ara", nextNode: "search_for_dragon" },
    { text: "Köyü koru", nextNode: "defend_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.suspect_elder = {
  title: "Yaşlıdan Şüphelenme",
  text: "Yaşlıdan şüpheleniyorsun. Onun söyledikleri doğru mu?",
  choices: [
    { text: "Sorgula", nextNode: "interrogate_elder" },
    { text: "Gözlemle", nextNode: "observe_elder" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.interrogate_elder = {
  title: "Yaşlıyı Sorgulama",
  text: "Yaşlıyı sorguluyorsun. O gerçeği söylüyor mu?",
  choices: [
    { text: "Gerçeği öğren", nextNode: "learn_truth" },
    { text: "Gözlemle", nextNode: "observe_elder" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.learn_truth = {
  title: "Gerçeği Öğrenme",
  text: "Yaşlıdan gerçeği öğrendin. Artık ne yapacağını biliyorsun.",
  choices: [
    { text: "Ejderhayı ara", nextNode: "search_for_dragon" },
    { text: "Köyü koru", nextNode: "defend_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.why_kill_me = {
  title: "Neden Beni Öldürmek İstiyorlar?",
  text: "Yaşlı: 'Sen çok güçlüsün. Kral senden korkuyor. Sen tahtı için tehdit oluşturuyorsun.'",
  choices: [
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Kaç", nextNode: "escape_secretly" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.protect_elder = {
  title: "Yaşlıyı Koruma",
  text: "Yaşlıyı korumaya karar verdin. Onu güvenli bir yere götürüyorsun.",
  choices: [
    { text: "Güvenli yere götür", nextNode: "take_to_safety" },
    { text: "Gizle", nextNode: "hide_elder" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.take_to_safety = {
  title: "Güvenli Yere Götürme",
  text: "Yaşlıyı güvenli bir yere götürdün. Artık güvende.",
  choices: [
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Köyü koru", nextNode: "defend_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.burn_treacherous_village = {
  title: "Hain Köyü Yakma",
  text: "Hain köyü yaktın. Artık kimse sana ihanet edemez.",
  choices: [
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Yeni köy kur", nextNode: "build_new_village" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.build_new_village = {
  title: "Yeni Köy Kurma",
  text: "Yeni bir köy kurdun. Bu köy sana sadık olacak.",
  choices: [
    { text: "Köyü yönet", nextNode: "rule_village" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.rule_village = {
  title: "Köyü Yönetme",
  text: "Köyü yönetiyorsun. Artık sen köyün liderisin.",
  choices: [
    { text: "Köyü büyüt", nextNode: "expand_village" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.expand_village = {
  title: "Köyü Büyütme",
  text: "Köyü büyüttün. Artık büyük bir kasaba oldu.",
  choices: [
    { text: "Kasabayı yönet", nextNode: "rule_town" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.rule_town = {
  title: "Kasabayı Yönetme",
  text: "Kasabayı yönetiyorsun. Artık sen kasabanın liderisin.",
  choices: [
    { text: "Kasabayı büyüt", nextNode: "expand_town" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.expand_town = {
  title: "Kasabayı Büyütme",
  text: "Kasabayı büyüttün. Artık büyük bir şehir oldu.",
  choices: [
    { text: "Şehri yönet", nextNode: "rule_city" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.rule_city = {
  title: "Şehri Yönetme",
  text: "Şehri yönetiyorsun. Artık sen şehrin liderisin.",
  choices: [
    { text: "Şehri büyüt", nextNode: "expand_city" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.expand_city = {
  title: "Şehri Büyütme",
  text: "Şehri büyüttün. Artık büyük bir krallık oldu.",
  choices: [
    { text: "Krallığı yönet", nextNode: "rule_kingdom" },
    { text: "Kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.rule_kingdom = {
  title: "Krallığı Yönetme",
  text: "Krallığı yönetiyorsun. Artık sen kral oldun.",
  choices: [
    { text: "Krallığı büyüt", nextNode: "expand_kingdom" },
    { text: "Eski kralı öldür", nextNode: "go_kill_king" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};
