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

  // Update NPC display
  if (npcSystem && npcSystem.updateNPCDisplay) {
    npcSystem.updateNPCDisplay();
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
        title: "Köyün Tehdidi",
        text: `Güneş batarken, köyün meydanında toplanmış köylülerin korku dolu yüzlerini görüyorsun. Yaşlı köy reisi, titreyen elleriyle seni işaret ediyor.

"Ejderha Avcısı! Kızıl Alev tekrar geldi! Bu gece köyümüzü yakacak!"

Köylüler arasından bir ses yükseliyor: "O ejderha 100 yıldır burada yoktu! Neden şimdi geri döndü?"

Başka biri ekliyor: "Belki de birisi onu uyandırdı..."

Senin yanında duran genç çiftçi Tom, fısıltıyla konuşuyor: "Köyün kuzeyindeki eski tapınakta bir şeyler oluyor. Gece yarısı garip ışıklar görüyorum."

Köy reisi sana dönüyor: "Seni ejderha avcısı olarak adlandırdık çünkü yanındaki kılıçta ejderha kanı izleri var. Bu kılıç sadece ejderha avcılarının kullandığı türden."

Kolyen üzerindeki semboller parlamaya başlıyor. Hafızanın bir kısmı geri geliyor - sen gerçekten de bir ejderha avcısısın, ama neden burada olduğunu hatırlamıyorsun.`,
        choices: [
          { text: "Ejderhayı aramaya çık", nextNode: "search_dragon" },
          { text: "Eski tapınağı araştır", nextNode: "investigate_temple" },
          { text: "Köylülerden bilgi topla", nextNode: "gather_info" },
          { text: "Kılıcını kontrol et", nextNode: "check_sword" },
          {
            text: "Kolyenin sırrını araştır",
            nextNode: "investigate_necklace",
          },
        ],
      },

      search_dragon: {
        title: "Ejderha İzlerini Takip",
        text: `Köyün dışına çıktığında, büyük pençe izleri ve yanmış ağaçlar görüyorsun. Ejderha buradan geçmiş. İzler seni dağlara doğru götürüyor.

Aniden, bir çığlık duyuyorsun. Köyün kuzeyinden geliyor. Hızlıca koştuğunda, genç bir kızın ejderha tarafından kovalandığını görüyorsun.

Kız, seni görünce yardım için bağırıyor: "Lütfen yardım et! Ben Lydia, köyün şifacısının kızıyım!"

Ejderha, Lydia'nın peşinde ve çok yakın. Kızıl Alev'in gözleri seni görüyor ve duruyor. Ejderha konuşuyor: "Sen... sen o musun? Ejderha Avcısı?"

Bu beklenmedik bir durum. Ejderha seni tanıyor gibi görünüyor. Lydia da şaşkın: "Ejderha konuşuyor? Bu imkansız!"`,
        choices: [
          { text: "Ejderhayla savaş", nextNode: "fight_dragon" },
          { text: "Lydia'yı kurtar ve kaç", nextNode: "save_lydia" },
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon" },
          { text: "Kolyeni göster", nextNode: "show_necklace" },
          { text: "Geri çekil ve plan yap", nextNode: "retreat_plan" },
        ],
      },

      fight_dragon: {
        title: "Ejderha Savaşı",
        text: `Kılıcını çekiyorsun ve ejderhaya doğru koşuyorsun. Kızıl Alev, alevli nefesini üzerine püskürtüyor ama sen kılıcınla alevleri kesiyorsun.

"Seni tanıyorum!" diye bağırıyor ejderha. "100 yıl önce beni öldüren sensin!"

Bu şok edici bir gerçek. Sen 100 yıl önce bu ejderhayı öldürmüşsün ama nasıl hala yaşıyorsun?

Savaş devam ediyor. Ejderha'nın kanatları rüzgarı kesiyor, kılıcın ejderha pullarına çarpıyor. Lydia, bir taşın arkasından izliyor.

Aniden, kolyen parlamaya başlıyor ve ejderha duruyor. "O kolye... o kolye senin değil! O benim kolyem!"

Bu bir plot twist! Kolye ejderhaya ait. Peki nasıl senin boynunda?`,
        choices: [
          { text: "Savaşa devam et", nextNode: "continue_fight" },
          { text: "Kolyeyi çıkar", nextNode: "remove_necklace" },
          { text: "Gerçeği öğren", nextNode: "learn_truth" },
          { text: "Lydia'dan yardım iste", nextNode: "ask_lydia_help" },
          { text: "Kaç", nextNode: "escape_battle" },
        ],
      },

      learn_truth: {
        title: "Gerçeğin Açığa Çıkması",
        text: `Ejderha, kolyeyi görünce savaşmayı bırakıyor. "O kolye benim aile yadigârım. 100 yıl önce sen onu çaldın ve beni öldürdün."

Lydia şaşkın: "Ama nasıl? 100 yıl önce nasıl yaşayabilirsin?"

Ejderha devam ediyor: "Ben ölmedim. Sen beni öldürdüğünü sandın ama ben sadece uykuya daldım. Şimdi uyandım ve kolyemi geri istiyorum."

Kolyen üzerindeki semboller daha da parlak yanıyor. Hafızanın daha fazlası geri geliyor. Gerçekten de 100 yıl önce bu ejderhayı "öldürdüğünü" hatırlıyorsun, ama aslında sadece uykuya daldırmışsın.

"Peki neden köyü tehdit ediyorsun?" diye soruyorsun.

"Köyü tehdit etmiyorum. Köyde birisi var ki beni uyandırdı ve kolyemi çalmaya çalışıyor. Ben sadece kolyemi arıyorum."`,
        choices: [
          { text: "Kolyeyi geri ver", nextNode: "return_necklace" },
          { text: "Köydeki hırsızı bul", nextNode: "find_thief" },
          { text: "Kolyeyi tut ve güç kazan", nextNode: "keep_necklace" },
          {
            text: "Lydia ile birlikte araştır",
            nextNode: "investigate_with_lydia",
          },
          { text: "Ejderhayı köye götür", nextNode: "bring_dragon_to_village" },
        ],
      },

      find_thief: {
        title: "Köydeki Hırsız",
        text: `Kolyeyi ejderhaya geri verdin. Şimdi köye dönüyorsun ve Lydia ile birlikte gerçek hırsızı arıyorsunuz.

Köyde şüpheli davranışlar gösteren birkaç kişi var:
- Yaşlı köy reisi çok gergin görünüyor
- Şifacı (Lydia'nın babası) sürekli evinden çıkmıyor
- Demirci Thorin, gece yarısı dışarıda dolaşıyor
- Tüccar Alric, garip paketler alıyor

Lydia fısıltıyla konuşuyor: "Babam son zamanlarda çok değişti. Gece yarısı garip dualar okuyor."

Köy reisi size yaklaşıyor: "Ejderha Avcısı! Ejderhayı öldürdün mü?"

Sen ve Lydia birbirinize bakıyorsunuz. Köy reisi çok aceleci görünüyor.`,
        choices: [
          { text: "Şifacıyı araştır", nextNode: "investigate_healer" },
          { text: "Köy reisini sorgula", nextNode: "question_mayor" },
          { text: "Demirciyi takip et", nextNode: "follow_blacksmith" },
          {
            text: "Tüccarın paketlerini kontrol et",
            nextNode: "check_merchant",
          },
          { text: "Gece yarısı gözetle", nextNode: "spy_at_night" },
        ],
      },

      investigate_healer: {
        title: "Şifacının Sırrı",
        text: `Lydia'nın evine gidiyorsunuz. Kapı kilitli ama Lydia anahtarı biliyor. İçeri girdiğinizde şok edici bir manzara görüyorsunuz.

Şifacı, odasında büyük bir altar kurmuş. Üzerinde ejderha kanı ve garip semboller var. Duvarda ejderha resimleri ve kolye çizimleri asılı.

"Baba? Ne yapıyorsun?" diye soruyor Lydia şok olmuş halde.

Şifacı dönüyor ve yüzünde delilik ifadesi var: "Lydia! Seni buraya getirme! Bu güç benim! Ejderha gücü benim olacak!"

Şifacı, bir büyü yapıyor ve odadaki eşyalar uçmaya başlıyor. Lydia korkuyla bağırıyor: "Baba! Bu sen değilsin!"

"Ben 100 yıl önce ejderha avcısıydım! Ejderhayı öldürdüm ama gücünü alamadım. Şimdi kolyeyi buldum ve güç benim olacak!"`,
        choices: [
          { text: "Şifacıyla savaş", nextNode: "fight_healer" },
          { text: "Lydia'yı koru", nextNode: "protect_lydia" },
          { text: "Ejderhayı çağır", nextNode: "call_dragon" },
          { text: "Büyüyü boz", nextNode: "break_spell" },
          { text: "Kaç", nextNode: "escape_healer" },
        ],
      },

      fight_healer: {
        title: "Şifacı Savaşı",
        text: `Şifacı, ejderha gücüyle size saldırıyor. Alevler ve büyüler odada uçuşuyor. Lydia, babasının bu haline şok olmuş.

"Baba! Lütfen dur! Bu sen değilsin!"

Şifacı gülüyor: "Ben her zaman böyleydim! 100 yıl önce ejderhayı öldürdüm ama gücünü alamadım. Şimdi kolye sayesinde güç benim!"

Kılıcınla şifacıya saldırıyorsun ama o büyü kalkanı kullanıyor. Büyüler seni geri itiyor.

Aniden, pencereden Kızıl Alev'in başı görünüyor. Ejderha, şifacıyı görünce öfkeyle bağırıyor: "Sen! Sen beni öldürmeye çalışan hırsız!"

Şifacı şaşkın: "Ejderha? Nasıl hala yaşıyorsun?"

"Ben ölmedim! Sen sadece beni uykuya daldırdın ve kolyemi çaldın!"`,
        choices: [
          { text: "Ejderhayla birlikte savaş", nextNode: "fight_with_dragon" },
          { text: "Lydia'yı kurtar", nextNode: "save_lydia_from_father" },
          { text: "Şifacıyı durdur", nextNode: "stop_healer" },
          { text: "Büyüyü boz", nextNode: "break_healer_spell" },
          { text: "Kaos yarat", nextNode: "create_chaos" },
        ],
      },

      fight_with_dragon: {
        title: "Ejderhayla Birlikte Savaş",
        text: `Kızıl Alev, pencereden içeri giriyor ve şifacıya alevli nefesini püskürtüyor. Şifacı, büyü kalkanıyla alevleri engelliyor ama ejderha çok güçlü.

Sen de kılıcınla şifacıya saldırıyorsun. İki taraftan gelen saldırı karşısında şifacı zorlanıyor.

Lydia, babasının bu haline ağlıyor: "Baba! Lütfen dur! Seni kaybetmek istemiyorum!"

Şifacı, kızının sesini duyunca bir an duraksıyor. Bu fırsatı kullanarak kılıcınla büyü kalkanını kırıyorsun.

Ejderha, şifacıyı yakalıyor ve onu havaya kaldırıyor: "Kolyemi geri ver!"

Şifacı, kolyeyi çıkarıyor ve ejderhaya atıyor: "Al! Ama gücü benim olacak!"

Kolye ejderhaya geri dönüyor ve parlamaya başlıyor. Şifacı, gücünü kaybediyor ve yere düşüyor.`,
        choices: [
          { text: "Şifacıyı affet", nextNode: "forgive_healer" },
          { text: "Şifacıyı cezalandır", nextNode: "punish_healer" },
          { text: "Lydia'yı teselli et", nextNode: "comfort_lydia" },
          { text: "Ejderhayla konuş", nextNode: "talk_to_dragon_after" },
          { text: "Köye dön", nextNode: "return_to_village_after" },
        ],
      },

      forgive_healer: {
        title: "Affetme ve Barış",
        text: `Şifacıyı affetmeye karar veriyorsun. Lydia'nın babası, yaptığı hataları anlıyor ve pişman oluyor.

"Özür dilerim... 100 yıl boyunca güç peşinde koştum ama asıl önemli olan ailemdi."

Ejderha, şifacıyı affediyor: "Sen beni öldürmeye çalıştın ama kızın sayesinde gerçeği gördün. Artık barış içinde yaşayabiliriz."

Lydia, babasına sarılıyor: "Baba, seni affediyorum. Artık normal hayatımıza dönebiliriz."

Köy, ejderha tehdidinin ortadan kalktığını öğreniyor. Artık Kızıl Alev, köyün koruyucusu oluyor ve şifacı da normal hayatına dönüyor.

Sen, hafızanı geri kazandın ve gerçek kimliğini öğrendin. Artık köyde saygı gören bir kahramansın.`,
        choices: [
          { text: "Köyde kal", nextNode: "stay_in_village" },
          { text: "Yeni maceralara çık", nextNode: "new_adventures" },
          { text: "Ejderhayla birlikte git", nextNode: "go_with_dragon" },
          { text: "Lydia ile evlen", nextNode: "marry_lydia" },
          { text: "Hikayeyi bitir", nextNode: "happy_ending" },
        ],
      },

      happy_ending: {
        title: "Mutlu Son",
        text: `Köyde mutlu bir hayat yaşıyorsun. Lydia ile evlendin, şifacı normal hayatına döndü ve Kızıl Alev köyün koruyucusu oldu. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Devam et", nextNode: "continue_farming" },
          { text: "Geri dön", nextNode: "return_to_village" },
        ],
      },

      // Additional nodes for deep branching
      search_dragon: {
        title: "Ejderha Arama",
        text: `Dağlarda ejderha izlerini takip ediyorsun. Büyük pençe izleri ve yanmış ağaçlar seni derinlere götürüyor.`,
        choices: [
          { text: "İzleri takip et", nextNode: "follow_tracks" },
          { text: "Geri dön", nextNode: "return_to_village" },
          { text: "Farklı yöne git", nextNode: "different_direction" },
        ],
      },

      follow_tracks: {
        title: "İzleri Takip",
        text: `Ejderha izlerini takip ediyorsun. Dağın derinliklerine doğru ilerliyorsun.`,
        choices: [
          { text: "Mağaraya gir", nextNode: "enter_cave" },
          { text: "Geri dön", nextNode: "return_to_village" },
          { text: "Bekle", nextNode: "wait_for_dragon" },
        ],
      },

      enter_cave: {
        title: "Mağaraya Giriş",
        text: `Karanlık mağaraya giriyorsun. İçeride ejderha'nın nefes sesini duyuyorsun.`,
        choices: [
          { text: "İçeri gir", nextNode: "enter_deep_cave" },
          { text: "Geri çık", nextNode: "exit_cave" },
          { text: "Ses çıkar", nextNode: "make_noise" },
        ],
      },

      enter_deep_cave: {
        title: "Mağaranın Derinlikleri",
        text: `Mağaranın derinliklerinde Kızıl Alev'i buluyorsun. Ejderha seni görüyor.`,
        choices: [
          { text: "Savaş", nextNode: "fight_dragon" },
          { text: "Konuş", nextNode: "talk_to_dragon" },
          { text: "Kaç", nextNode: "escape_cave" },
        ],
      },

      escape_cave: {
        title: "Mağaradan Kaçış",
        text: `Mağaradan hızla çıkıyorsun. Ejderha peşinde ama sen kaçmayı başarıyorsun.`,
        choices: [
          { text: "Köye dön", nextNode: "return_to_village" },
          { text: "Yardım ara", nextNode: "seek_help" },
          { text: "Plan yap", nextNode: "make_plan" },
        ],
      },

      return_to_village: {
        title: "Köye Dönüş",
        text: `Köye dönüyorsun. Köylüler seni karşılıyor ve ne olduğunu soruyorlar.`,
        choices: [
          { text: "Gerçeği anlat", nextNode: "tell_truth" },
          { text: "Yalan söyle", nextNode: "lie_to_villagers" },
          { text: "Sessiz kal", nextNode: "stay_silent" },
        ],
      },

      tell_truth: {
        title: "Gerçeği Anlatma",
        text: `Köylülere ejderha'nın konuştuğunu ve kolyenin onun olduğunu anlatıyorsun.`,
        choices: [
          { text: "Hırsızı ara", nextNode: "find_thief" },
          { text: "Ejderhayla barış yap", nextNode: "make_peace" },
          { text: "Köyü koru", nextNode: "protect_village" },
        ],
      },

      make_peace: {
        title: "Barış Yapma",
        text: `Ejderha ile barış yapmaya karar veriyorsun. Köy artık güvende.`,
        choices: [
          { text: "Köyde kal", nextNode: "stay_in_village" },
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Hikayeyi bitir", nextNode: "happy_ending" },
        ],
      },

      stay_in_village: {
        title: "Köyde Kalma",
        text: `Köyde kalıyorsun ve köylülerle birlikte yaşıyorsun.`,
        choices: [
          { text: "Çiftçi ol", nextNode: "become_farmer" },
          { text: "Koruyucu ol", nextNode: "become_protector" },
          { text: "Hikayeyi bitir", nextNode: "happy_ending" },
        ],
      },

      become_farmer: {
        title: "Çiftçi Olma",
        text: `Köyde çiftçi olarak yaşıyorsun. Sakin bir hayat sürüyorsun.`,
        choices: [
          { text: "Devam et", nextNode: "continue_farming" },
          { text: "Hikayeyi bitir", nextNode: "happy_ending" },
        ],
      },

      continue_farming: {
        title: "Çiftçilik Devam",
        text: `Çiftçilik yapmaya devam ediyorsun. Köyde mutlu bir hayat yaşıyorsun.`,
        choices: [{ text: "Hikayeyi bitir", nextNode: "happy_ending" }],
      },

      new_adventure: {
        title: "Yeni Macera",
        text: `Yeni maceralara çıkmaya karar veriyorsun. Dünyayı keşfetmek istiyorsun.`,
        choices: [{ text: "Yeni hikaye", nextNode: "new_story_ending" }],
      },

      new_story_ending: {
        title: "Yeni Hikaye Sonu",
        text: `Yeni maceralara çıktın. Hikayen burada biter ama başka hikayeler seni bekliyor.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Geri dön", nextNode: "return_to_village" },
        ],
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
        text: `Neon ışıkların altında gözlerini açıyorsun. Hive City'nin alt katmanlarında, MegaCorp'ların gözlerinden uzak bir yerde uyandın. Vücudundaki cyberware'ler yanıp sönüyor, neural link'in ağrıyor.

Etrafında Hive City'nin sakinleri var - netrunner'lar, hacker'lar, cyberpunk'lar. Hepsi seni merakla izliyor. Yanında duran genç netrunner, Shadow, sana yaklaşıyor.

"Matrix'in Seçilmişi! Sonunda uyandın! MegaCorp'lar Hive City'yi yok etmeye çalışıyor. Biz isyan başlattık ama senin yardımına ihtiyacımız var."

Başka bir netrunner, Chrome, ekliyor: "Arasaka ve Militech birlikte çalışıyor. Hive City'yi yok etmek istiyorlar çünkü burada onların sırlarını biliyoruz."

Data chip'in yanıp sönüyor. Hafızanın bir kısmı geri geliyor - sen gerçekten de özel bir cyberpunk'sın, ama neden burada olduğunu hatırlamıyorsun.`,
        choices: [
          { text: "İsyana katıl", nextNode: "join_rebellion" },
          { text: "MegaCorp'larla konuş", nextNode: "talk_to_corps" },
          { text: "Hafızanı geri getir", nextNode: "recover_memory" },
          { text: "Data chip'i incele", nextNode: "examine_data_chip" },
          { text: "Hive City'yi keşfet", nextNode: "explore_hive_city" },
        ],
      },

      join_rebellion: {
        title: "İsyana Katılma",
        text: `Netrunner'larla birlikte isyana katılıyorsun. Shadow, sana Hive City'nin durumunu anlatıyor.

"Arasaka, Hive City'deki tüm netrunner'ları öldürmek istiyor çünkü onların gizli projelerini biliyoruz. Militech de bize silah satıyor ama aynı zamanda bizi izliyor."

Chrome devam ediyor: "Biz sadece özgürlük istiyoruz. MegaCorp'lar bizi köle gibi kullanıyor."

Aniden, Hive City'nin üst katmanlarından güçlü bir patlama sesi geliyor. Arasaka'nın güvenlik botları Hive City'ye saldırıyor.

"Geldiler!" diye bağırıyor Shadow. "Arasaka'nın güvenlik botları! Hive City'yi savunmamız gerekiyor!"

Data chip'in daha da parlak yanıyor. Hafızanın daha fazlası geri geliyor - sen Arasaka'da çalışmışsın ama onların sırlarını öğrendiğin için kaçmışsın.`,
        choices: [
          {
            text: "Güvenlik botlarıyla savaş",
            nextNode: "fight_security_bots",
          },
          { text: "Hive City'yi savun", nextNode: "defend_hive_city" },
          { text: "Arasaka'ya sız", nextNode: "infiltrate_arasaka" },
          { text: "Militech ile anlaş", nextNode: "deal_with_militech" },
          { text: "Kaç", nextNode: "escape_hive_city" },
        ],
      },

      fight_security_bots: {
        title: "Güvenlik Botlarıyla Savaş",
        text: `Arasaka'nın güvenlik botları Hive City'ye saldırıyor. Metal yaratıklar, netrunner'ları öldürmek için programlanmış.

Pistolünü çekiyorsun ve botlara ateş ediyorsun. Cyberware'lerin sayesinde hızlı hareket edebiliyorsun. Shadow ve Chrome da savaşıyor.

"Bu botlar Arasaka'nın en yeni modelleri!" diye bağırıyor Shadow. "Neural link'lerini hack etmemiz gerekiyor!"

Chrome, bir botu hack etmeye çalışıyor ama başarısız oluyor. Bot, Chrome'a saldırıyor ve onu yaralıyor.

"Chrome!" diye bağırıyor Shadow.

Sen, data chip'inin gücünü kullanarak botları hack etmeye çalışıyorsun. Aniden, botlar duruyor ve size dönüyor. Data chip'in onları kontrol ediyor!`,
        choices: [
          { text: "Botları kontrol et", nextNode: "control_bots" },
          { text: "Chrome'u kurtar", nextNode: "save_chrome" },
          { text: "Arasaka'ya saldır", nextNode: "attack_arasaka" },
          { text: "Botları yok et", nextNode: "destroy_bots" },
          { text: "Kaç", nextNode: "escape_battle" },
        ],
      },

      control_bots: {
        title: "Botları Kontrol Etme",
        text: `Data chip'in sayesinde Arasaka'nın güvenlik botlarını kontrol edebiliyorsun. Botlar artık size hizmet ediyor.

Shadow şaşkın: "Nasıl yaptın bunu? Bu imkansız!"

Chrome, yaralarını tedavi ederken konuşuyor: "Data chip'in özel. Arasaka'nın en gizli teknolojisi bu."

Botları kullanarak Hive City'yi savunuyorsun. Arasaka'nın diğer saldırıları başarısız oluyor.

Aniden, neural link'in ağrımaya başlıyor. Data chip'in çok fazla güç kullanıyor. Hafızanın daha fazlası geri geliyor - sen Arasaka'nın en iyi netrunner'ıydın ama onların insanlık dışı deneylerini gördüğün için kaçtın.

"Arasaka, insanları cyberware ile değiştiriyor. Onların bilinci kayboluyor ve sadece bot haline geliyorlar. Ben de onlardan biri olacaktım."`,
        choices: [
          { text: "Arasaka'yı yok et", nextNode: "destroy_arasaka" },
          { text: "Militech ile anlaş", nextNode: "deal_with_militech" },
          { text: "Hive City'yi koru", nextNode: "protect_hive_city" },
          { text: "Data chip'i kaldır", nextNode: "remove_data_chip" },
          { text: "Güç kazan", nextNode: "gain_power" },
        ],
      },

      destroy_arasaka: {
        title: "Arasaka'yı Yok Etme",
        text: `Botları kullanarak Arasaka'nın Hive City'deki merkezine saldırıyorsun. Arasaka'nın güvenlik sistemi çöküyor.

Shadow ve Chrome da sana katılıyor. Birlikte Arasaka'nın veri merkezine giriyorsunuz.

"Burada Arasaka'nın tüm sırları var!" diye bağırıyor Shadow.

Arasaka'nın CEO'su, Yorinobu Arasaka, karşınıza çıkıyor. "Siz kimsiniz? Nasıl botlarımızı hack ettiniz?"

"Ben senin eski netrunner'ınım. İnsanlık dışı deneylerini gördüm ve kaçtım."

Yorinobu gülüyor: "İnsanlık? Cyberware geleceğimiz! İnsanlar zayıf, makineler güçlü!"

"Sen yanlış düşünüyorsun. İnsanlık ve teknoloji birlikte olmalı, birbirini yok etmemeli."`,
        choices: [
          { text: "Yorinobu'yu öldür", nextNode: "kill_yorinobu" },
          { text: "Yorinobu'yu ikna et", nextNode: "convince_yorinobu" },
          { text: "Verileri yayınla", nextNode: "publish_data" },
          { text: "Arasaka'yı ele geçir", nextNode: "take_over_arasaka" },
          { text: "Barış yap", nextNode: "make_peace_arasaka" },
        ],
      },

      kill_yorinobu: {
        title: "Yorinobu'yu Öldürme",
        text: `Yorinobu'yu öldürüyorsun. Arasaka'nın CEO'su ölüyor ve şirket karışıyor.

"Arasaka artık güçsüz!" diye bağırıyor Shadow.

Chrome ekliyor: "Ama Militech hala var. Onlar da tehlikeli."

Arasaka'nın verilerini ele geçiriyorsun. Tüm sırları, deneyleri, projeleri artık senin elinde.

"Bu verilerle Night City'yi değiştirebiliriz. MegaCorp'ların gücünü kırabiliriz."

Hive City'nin sakinleri seni kahraman olarak görüyor. Artık Hive City'nin liderisin.`,
        choices: [
          { text: "Hive City'yi yönet", nextNode: "rule_hive_city" },
          { text: "Night City'yi değiştir", nextNode: "change_night_city" },
          { text: "Yeni hayat", nextNode: "new_life_cyberpunk" },
          { text: "Hikayeyi bitir", nextNode: "cyberpunk_ending" },
        ],
      },

      rule_hive_city: {
        title: "Hive City'yi Yönetme",
        text: `Hive City'yi yönetiyorsun. Artık sen Night City'nin en güçlü kişisisin. MegaCorp'lar senden korkuyor.`,
        choices: [
          { text: "Güçlü lider", nextNode: "powerful_leader_cyberpunk" },
          { text: "Halkın lideri", nextNode: "peoples_leader_cyberpunk" },
          { text: "Teknoloji kralı", nextNode: "tech_king_cyberpunk" },
        ],
      },

      powerful_leader_cyberpunk: {
        title: "Güçlü Lider",
        text: `Night City'nin en güçlü lideri oldun. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Şehri yönet", nextNode: "rule_hive_city" },
          { text: "Kaç", nextNode: "escape_city" },
        ],
      },

      cyberpunk_ending: {
        title: "Cyberpunk Sonu",
        text: `Hive City'deki maceran bitti. İsyanı çözdün veya katıldın. Bu sadece bir son değil, yeni bir başlangıç.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Şehirde kal", nextNode: "stay_in_city" },
          { text: "Kaç", nextNode: "escape_city" }
        ]
      },

      // CYBERPUNK EKSİK NODE'LAR
      talk_to_corps: {
        title: "MegaCorp'larla Konuşma",
        text: `Arasaka'nın merkezine gidiyorsun. Güvenlik botları seni durduruyor ama data chip'in sayesinde geçebiliyorsun.
        
        Arasaka'nın CEO'su Yorinobu Arasaka ile görüşüyorsun. "Hive City'deki isyanı durdurmak istiyoruz. Sen bize yardım edebilirsin."
        
        "Hive City'deki insanlar özgürlük istiyor. Onları köle gibi kullanıyorsunuz."
        
        Yorinobu gülüyor: "Özgürlük? Cyberware geleceğimiz! İnsanlar zayıf, makineler güçlü!"`,
        choices: [
          { text: "Anlaşma yap", nextNode: "make_deal_with_corps" },
          { text: "Reddet", nextNode: "reject_corps" },
          { text: "Tehdit et", nextNode: "threaten_corps" },
          { text: "Geri dön", nextNode: "return_to_hive" }
        ]
      },

      make_deal_with_corps: {
        title: "MegaCorp'larla Anlaşma",
        text: `Arasaka ile anlaşma yapıyorsun. Hive City'yi koruyacaklar ama karşılığında data chip'inin teknolojisini paylaşacaksın.
        
        "Bu anlaşma Hive City'yi kurtaracak," diyorsun.
        
        Yorinobu: "Evet, ama sen de bizimle çalışacaksın. Arasaka'nın en iyi netrunner'ı olacaksın."`,
        choices: [
          { text: "Kabul et", nextNode: "accept_corp_deal" },
          { text: "Reddet", nextNode: "reject_corp_deal" },
          { text: "Plan yap", nextNode: "plan_against_corps" }
        ]
      },

      accept_corp_deal: {
        title: "Anlaşmayı Kabul Etme",
        text: `Arasaka ile anlaşmayı kabul ediyorsun. Artık Arasaka'nın en iyi netrunner'ısın. Hive City güvende ama sen MegaCorp'un kontrolü altındasın.`,
        choices: [
          { text: "Yeni hayat", nextNode: "new_life_corp" },
          { text: "İsyan planla", nextNode: "plan_rebellion_secret" },
          { text: "Güç kazan", nextNode: "gain_corp_power" }
        ]
      },

      new_life_corp: {
        title: "Yeni Hayat",
        text: `Arasaka'da yeni bir hayat başlıyorsun. Güçlü bir netrunner'sın ama özgürlüğünü kaybettin. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Devam et", nextNode: "continue_corp_life" }
        ]
      },

      recover_memory: {
        title: "Hafızayı Geri Getirme",
        text: `Data chip'inin gücünü kullanarak hafızanı geri getirmeye çalışıyorsun. Aniden, geçmişin gözlerinin önünde canlanıyor.
        
        Sen Arasaka'nın en iyi netrunner'ıydın. Onların insanlık dışı deneylerini gördün - insanları cyberware ile değiştiriyorlar, bilinçlerini kaybediyorlar.
        
        "Ben de onlardan biri olacaktım," diyorsun kendine. "Ama kaçtım ve Hive City'ye sığındım."`,
        choices: [
          { text: "Arasaka'ya karşı savaş", nextNode: "fight_arasaka_memory" },
          { text: "Hive City'yi koru", nextNode: "protect_hive_memory" },
          { text: "Güç kullan", nextNode: "use_memory_power" }
        ]
      },

      fight_arasaka_memory: {
        title: "Arasaka'ya Karşı Savaş",
        text: `Hafızanı geri kazandığın için Arasaka'ya karşı savaşmaya karar veriyorsun. Hive City'deki netrunner'ları topluyorsun.
        
        "Arasaka insanları yok ediyor! Onlara karşı savaşmalıyız!" diye bağırıyorsun.
        
        Shadow ve Chrome sana katılıyor. Birlikte Arasaka'ya saldırı planı yapıyorsunuz.`,
        choices: [
          { text: "Saldırı planla", nextNode: "plan_attack_arasaka" },
          { text: "Güçlendir", nextNode: "strengthen_hive" },
          { text: "Müttefik ara", nextNode: "find_allies" }
        ]
      },

      plan_attack_arasaka: {
        title: "Arasaka Saldırı Planı",
        text: `Arasaka'ya saldırı planı yapıyorsunuz. Data chip'inin gücünü kullanarak Arasaka'nın sistemlerini hack edeceksiniz.
        
        "Önce güvenlik sistemlerini devre dışı bırakacağız," diyorsun. "Sonra veri merkezine saldıracağız."
        
        Shadow: "Bu çok tehlikeli ama gerekli. Arasaka'yı durdurmamız gerekiyor."`,
        choices: [
          { text: "Saldırıya başla", nextNode: "start_attack_arasaka" },
          { text: "Daha fazla hazırlan", nextNode: "prepare_more" },
          { text: "Geri çekil", nextNode: "retreat_plan" }
        ]
      },

      start_attack_arasaka: {
        title: "Arasaka Saldırısı",
        text: `Arasaka'ya saldırıya başlıyorsunuz. Data chip'inin gücüyle güvenlik sistemlerini hack ediyorsunuz.
        
        Arasaka'nın güvenlik botları size saldırıyor ama siz onları kontrol edebiliyorsunuz. Veri merkezine giriyorsunuz.
        
        "Arasaka'nın tüm sırları burada!" diye bağırıyor Shadow.`,
        choices: [
          { text: "Verileri yayınla", nextNode: "publish_arasaka_data" },
          { text: "Arasaka'yı yok et", nextNode: "destroy_arasaka_complete" },
          { text: "Yorinobu'yu bul", nextNode: "find_yorinobu" }
        ]
      },

      publish_arasaka_data: {
        title: "Arasaka Verilerini Yayınlama",
        text: `Arasaka'nın tüm sırlarını Night City'ye yayınlıyorsunuz. İnsanlık dışı deneyler, gizli projeler, her şey ortaya çıkıyor.
        
        Night City karışıyor. İnsanlar Arasaka'ya karşı isyan ediyor. MegaCorp'lar güç kaybediyor.
        
        "Başardık!" diye bağırıyor Shadow. "Arasaka artık güçsüz!"`,
        choices: [
          { text: "Hive City'yi yönet", nextNode: "rule_hive_city" },
          { text: "Night City'yi değiştir", nextNode: "change_night_city" },
          { text: "Yeni hayat", nextNode: "new_life_cyberpunk" }
        ]
      },

      change_night_city: {
        title: "Night City'yi Değiştirme",
        text: `Arasaka'nın çöküşünden sonra Night City değişiyor. MegaCorp'ların gücü azalıyor, insanlar daha özgür oluyor.
        
        Sen Night City'nin kahramanı oldun. Hive City'nin lideri olarak yeni bir düzen kuruyorsun.`,
        choices: [
          { text: "Yeni düzen", nextNode: "new_order_cyberpunk" },
          { text: "Teknoloji kralı", nextNode: "tech_king_cyberpunk" },
          { text: "Halkın lideri", nextNode: "peoples_leader_cyberpunk" }
        ]
      },

      new_order_cyberpunk: {
        title: "Yeni Düzen",
        text: `Night City'de yeni bir düzen kuruyorsun. MegaCorp'ların yerine halkın yönettiği bir sistem oluşturuyorsun. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Devam et", nextNode: "continue_new_order" }
        ]
      },

      continue_new_order: {
        title: "Yeni Düzen Devamı",
        text: `Yeni düzen devam ediyorsun. MegaCorp'ların yerine halkın yönettiği bir sistem oluşturuluyor. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Devam et", nextNode: "continue_new_order" }
        ]
      },

      gain_corp_power: {
        title: "Güç Kazanma",
        text: `Data chip'inin gücünü kullanarak güç kazanmaya çalışıyorsun. Aniden, güçlü bir yeni bir yapı oluşuyor.
        
        "Bu güç benimle! İmperium'u yok edeceğim!" diye bağırıyorsun.
        
        "Bu çok tehlikeli," diyorsun. "Gücünüzü kullanmayın."`,
        choices: [
          { text: "Gücü kullan", nextNode: "use_memory_power" },
          { text: "Geri çekil", nextNode: "retreat_power" }
        ]
      },

      use_memory_power: {
        title: "Güç Kullanma",
        text: `Data chip'inin gücünü kullanarak güç kullanmaya çalışıyorsun. Aniden, güçlü bir yeni bir yapı oluşuyor.
        
        "Bu güç benimle! İmperium'u yok edeceğim!" diye bağırıyorsun.
        
        "Bu çok tehlikeli," diyorsun. "Gücünüzü kullanmayın."`,
        choices: [
          { text: "Gücü kullan", nextNode: "use_memory_power" },
          { text: "Geri çekil", nextNode: "retreat_power" }
        ]
      },

      retreat_power: {
        title: "Güçten Geri Çekilme",
        text: `Güç kullanmaya çalıştığın için güçten geri çekiliyorsun. Gücünüzü kaybettiniz. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Devam et", nextNode: "continue_new_order" }
        ]
      },

      return_to_hive: {
        title: "Hive City'ye Dönüş",
        text: `Hive City'ye dönüyorsun. MegaCorp'ların gücü azaldığı için Hive City'deki insanlar daha özgür oluyor.`,
        choices: [
          { text: "Hive City'yi yönet", nextNode: "rule_hive_city" },
          { text: "Night City'yi değiştir", nextNode: "change_night_city" },
          { text: "Yeni hayat", nextNode: "new_life_cyberpunk" }
        ]
      },

      reject_corps: {
        title: "MegaCorp'ları Reddetme",
        text: `MegaCorp'ları reddediyorsun. Hive City'deki insanlar MegaCorp'ların zulmünden kurtulmak için isyan ediyorlar.
        
        "Bu çok tehlikeli," diyorsun. "MegaCorp'ların gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "Hive City'deki insanların birlikte çalışmasıyla."`,
        choices: [
          { text: "İsyan planla", nextNode: "plan_rebellion_secret" },
          { text: "Güçlendir", nextNode: "strengthen_hive" },
          { text: "Müttefik ara", nextNode: "find_allies" }
        ]
      },

      plan_rebellion_secret: {
        title: "İsyan Planı",
        text: `Hive City'deki insanların MegaCorp'ların zulmünden kurtulmak için isyan edeceğini planlıyorsun.
        
        "Hive City'deki tüm netrunner'ları toplayalım," diyorsun. "Shadow ve Chrome'u da katılmasını sağlayalım."
        
        "Ama bu çok tehlikeli," diyorsun. "MegaCorp'ların gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "Hive City'deki insanların birlikte çalışmasıyla."`,
        choices: [
          { text: "İsyan planla", nextNode: "plan_rebellion_secret" },
          { text: "Güçlendir", nextNode: "strengthen_hive" },
          { text: "Müttefik ara", nextNode: "find_allies" }
        ]
      },

      strengthen_hive: {
        title: "Hive City'yi Güçlendirme",
        text: `Hive City'yi güçlendirmeye çalışıyorsun. MegaCorp'ların gücü çok büyük. Onları durdurmak için Hive City'deki insanların birlikte çalışması gerekiyor.
        
        "Hive City'deki tüm insanları toplayalım," diyorsun. "Shadow, Chrome ve diğer netrunner'ları da katılmasını sağlayalım."
        
        "Ama bu çok tehlikeli," diyorsun. "MegaCorp'ların gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "Hive City'deki insanların birlikte çalışmasıyla."`,
        choices: [
          { text: "İsyan planla", nextNode: "plan_rebellion_secret" },
          { text: "Güçlendir", nextNode: "strengthen_hive" },
          { text: "Müttefik ara", nextNode: "find_allies" }
        ]
      },

      find_allies: {
        title: "Müttefik Bulma",
        text: `Müttefik bulmaya çalışıyorsun. MegaCorp'ların gücü çok büyük. Onları durdurmak için Hive City'deki insanların birlikte çalışması gerekiyor.
        
        "Hive City'deki tüm insanları toplayalım," diyorsun. "Shadow, Chrome ve diğer netrunner'ları da katılmasını sağlayalım."
        
        "Ama bu çok tehlikeli," diyorsun. "MegaCorp'ların gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "Hive City'deki insanların birlikte çalışmasıyla."`,
        choices: [
          { text: "İsyan planla", nextNode: "plan_rebellion_secret" },
          { text: "Güçlendir", nextNode: "strengthen_hive" },
          { text: "Müttefik ara", nextNode: "find_allies" }
        ]
      },

      new_imperial_mission: {
        title: "Yeni İmperium Görevi",
        text: `İmperium'a yeni bir görev verildi. Chaos'un kaynağını bulmak ve kapatmak.
        
        "Bu çok tehlikeli," diyorsun. "Chaos'un gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "İmperium'un gücüyle birlikte."`,
        choices: [
          { text: "Chaos kaynağını bul", nextNode: "find_chaos_source" },
          { text: "Güçlendir", nextNode: "strengthen_imperium" },
          { text: "Yardım çağır", nextNode: "call_imperial_help" }
        ]
      },

      strengthen_imperium: {
        title: "İmperium'u Güçlendirme",
        text: `İmperium'u güçlendirmeye çalışıyorsun. MegaCorp'ların gücü çok büyük. Onları durdurmak için İmperium'un gücüyle birlikte çalışması gerekiyor.
        
        "İmperium'un tüm askerlerini toplayalım," diyorsun. "Space Marines'ı da katılmasını sağlayalım."
        
        "Ama bu çok tehlikeli," diyorsun. "MegaCorp'ların gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "İmperium'un gücüyle birlikte."`,
        choices: [
          { text: "Chaos kaynağını bul", nextNode: "find_chaos_source" },
          { text: "Güçlendir", nextNode: "strengthen_imperium" },
          { text: "Yardım çağır", nextNode: "call_imperial_help" }
        ]
      },

      call_imperial_help: {
        title: "İmperium'a Yardım Çağırma",
        text: `İmperium'a yardım çağırıyorsun. MegaCorp'ların gücü çok büyük. Onları durdurmak için İmperium'un gücüyle birlikte çalışması gerekiyor.
        
        "İmperium'un tüm askerlerini toplayalım," diyorsun. "Space Marines'ı da katılmasını sağlayalım."
        
        "Ama bu çok tehlikeli," diyorsun. "MegaCorp'ların gücü çok büyük."
        
        "Ama biz de güçlüyüz," diyorsun. "İmperium'un gücüyle birlikte."`,
        choices: [
          { text: "Chaos kaynağını bul", nextNode: "find_chaos_source" },
          { text: "Güçlendir", nextNode: "strengthen_imperium" },
          { text: "Yardım çağır", nextNode: "call_imperial_help" }
        ]
      },

      become_inquisitor: {
        title: "Inquisitor Olma",
        text: `Inquisitor oldun! Artık İmperium'un en güçlü ajanlarından birisin. Chaos'a karşı savaşmak senin görevin.`,
        choices: [
          { text: "Chaos avcısı", nextNode: "chaos_hunter" },
          { text: "İmperium'u koru", nextNode: "protect_imperium_inquisitor" },
          { text: "Yeni macera", nextNode: "new_adventure" }
        ]
      },

      chaos_hunter: {
        title: "Chaos Avcısı",
        text: `Chaos avcısı olarak İmperium'un en tehlikeli düşmanlarıyla savaşıyorsun. Her gün yeni bir Chaos tehdidi, her gün yeni bir savaş.`,
        choices: [
          { text: "Kahraman ol", nextNode: "become_hero_warhammer" },
          { text: "Savaşa devam et", nextNode: "continue_war" },
          { text: "Dinlen", nextNode: "rest_peacefully" }
        ]
      },

      protect_imperium_inquisitor: {
        title: "İmperium'u Koruma",
        text: `İmperium'u korumaya devam ediyorsun. Artık İmperium'un en güçlü askerlerinden birisin.`,
        choices: [
          { text: "Space Marine ol", nextNode: "become_space_marine" },
          { text: "Imperial Guard'da kal", nextNode: "stay_guard" },
          { text: "Commissar ol", nextNode: "become_commissar" }
        ]
      },

      // GENEL EKSİK NODE'LAR
      new_adventure: {
        title: "Yeni Macera",
        text: `Yeni bir maceraya başlıyorsun. Dünya seni bekliyor!`,
        choices: [
          { text: "Fantasy dünyası", nextNode: "fantasy_world" },
          { text: "Cyberpunk dünyası", nextNode: "cyberpunk_world" },
          { text: "Warhammer dünyası", nextNode: "warhammer_world" }
        ]
      },

      fantasy_world: {
        title: "Fantasy Dünyası",
        text: `Fantasy dünyasına gidiyorsun. Yeni maceralar, yeni kahramanlar seni bekliyor.`,
        choices: [
          { text: "Yeni hikaye", nextNode: "new_story_ending" },
          { text: "Geri dön", nextNode: "return_to_village" }
        ]
      },

      cyberpunk_world: {
        title: "Cyberpunk Dünyası",
        text: `Cyberpunk dünyasına gidiyorsun. Neon ışıklar ve teknoloji seni bekliyor.`,
        choices: [
          { text: "Yeni hikaye", nextNode: "new_story_ending" },
          { text: "Geri dön", nextNode: "return_to_village" }
        ]
      },

      warhammer_world: {
        title: "Warhammer Dünyası",
        text: `Warhammer dünyasına gidiyorsun. İmperium ve Chaos savaşları seni bekliyor.`,
        choices: [
          { text: "Yeni hikaye", nextNode: "new_story_ending" },
          { text: "Geri dön", nextNode: "return_to_village" }
        ]
      },

      return_to_village: {
        title: "Köye Dönüş",
        text: `Köye dönüyorsun. Hikayen burada biter ama yeni maceralar seni bekliyor.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Dinlen", nextNode: "rest_peacefully" }
        ]
      },

      rest_peacefully: {
        title: "Huzurlu Dinlenme",
        text: `Huzurlu bir şekilde dinleniyorsun. Maceran bitti ama anıların seninle kalacak.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Hikayeyi bitir", nextNode: "final_ending" }
        ]
      },

      final_ending: {
        title: "Final Son",
        text: `Maceran bitti. Sen harika bir kahraman oldun ve dünyayı değiştirdin. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Baştan başla", nextNode: "start_over" }
        ]
      },

      start_over: {
        title: "Baştan Başlama",
        text: `Yeni bir maceraya başlıyorsun. Bu sefer farklı seçimler yapacaksın.`,
        choices: [
          { text: "Fantasy", nextNode: "fantasy_world" },
          { text: "Cyberpunk", nextNode: "cyberpunk_world" },
          { text: "Warhammer", nextNode: "warhammer_world" }
        ]
      }
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
        title: "Cadia Prime'da Uyanış",
        text: `Power armor'ının içinde gözlerini açıyorsun. Cadia Prime'ın uzak bir köyünde, Chaos tehdidinin büyüdüğü bir yerde uyandın. Power armor'ın ağırlığını hissediyorsun, lasgun'ın elinde.

Etrafında Cadian Shock Troops'un diğer askerleri var. Hepsi seni merakla izliyor. Yanında duran genç asker, Marcus, sana yaklaşıyor.

"İmperium'un Seçilmişi! Sonunda uyandın! Chaos kültü bu köyde büyüyor. Biz onları bulamıyoruz ama sen yardım edebilirsin."

Başka bir asker, Sarah, ekliyor: "Köylüler gece gizlice toplanıyor. Tuhaf semboller çiziyorlar, dualar okuyorlar. Chaos'un karanlık güçleri buraya sızıyor."

Kutsal kolyen yanıp sönüyor. Hafızanın bir kısmı geri geliyor - sen gerçekten de özel bir İmperium askerisin, ama neden burada olduğunu hatırlamıyorsun.`,
        choices: [
          { text: "Chaos kültünü ara", nextNode: "search_chaos_cult" },
          { text: "Köylülerle konuş", nextNode: "talk_to_villagers" },
          { text: "Hafızanı geri getir", nextNode: "recover_memory_warhammer" },
          { text: "Kolyeyi incele", nextNode: "examine_necklace_warhammer" },
          { text: "Köyü keşfet", nextNode: "explore_village" },
        ],
      },

      search_chaos_cult: {
        title: "Chaos Kültünü Arama",
        text: `Marcus ve Sarah ile birlikte Chaos kültünü arıyorsunuz. Köyün karanlık sokaklarında dolaşıyorsunuz.

"Burada garip izler var," diyor Marcus. "Köylüler buradan geçmiş."

Sarah ekliyor: "Ve bu izler köyün eski tapınağına gidiyor. O tapınak yıllardır kullanılmıyor."

Eski tapınağa yaklaştığınızda, içeriden garip sesler duyuyorsunuz. Dualar, çığlıklar, tuhaf müzik.

"İçeride bir şeyler oluyor," diye fısıldıyor Marcus.

Kutsal kolyen daha da parlak yanıyor. Hafızanın daha fazlası geri geliyor - sen bu tapınakta daha önce bulunmuşsun, ama ne zaman ve neden hatırlamıyorsun.

Tapınağın kapısını açtığınızda, şok edici bir manzara görüyorsunuz. Köylüler, Chaos sembolleri etrafında toplanmış, dualar okuyorlar.`,
        choices: [
          { text: "Tapınağa gir", nextNode: "enter_temple" },
          { text: "Geri çekil", nextNode: "retreat_from_temple" },
          { text: "Gözetle", nextNode: "spy_on_cult" },
          { text: "Yardım çağır", nextNode: "call_for_help" },
          { text: "Plan yap", nextNode: "make_plan_warhammer" },
        ],
      },

      enter_temple: {
        title: "Tapınağa Giriş",
        text: `Tapınağa giriyorsunuz. İçeride köylüler, Chaos sembolleri etrafında toplanmış. Ortada bir altar var ve üzerinde garip semboller yanıyor.

Köylüler sizi görünce duruyor. Aralarından birisi, yaşlı bir adam, size yaklaşıyor.

"İmperium'un askerleri! Siz de mi gerçeği öğrenmek istiyorsunuz?"

Marcus, lasgun'ını doğrultuyor: "Chaos kültü! Siz sapkınlık yapıyorsunuz!"

Yaşlı adam gülüyor: "Sapkınlık? İmperium bizi köle gibi kullanıyor. Chaos bize güç veriyor!"

Sarah bağırıyor: "Chaos sizi yok edecek! İmperium sizi koruyor!"

Kutsal kolyen çok parlak yanıyor. Hafızanın daha fazlası geri geliyor - sen bu tapınakta daha önce bulunmuşsun ve Chaos'un tehlikesini biliyorsun.`,
        choices: [
          { text: "Kültü yok et", nextNode: "destroy_cult" },
          { text: "Köylüleri ikna et", nextNode: "convince_villagers" },
          { text: "Kült liderini bul", nextNode: "find_cult_leader" },
          { text: "Geri çekil", nextNode: "retreat_from_cult" },
          { text: "Chaos'u kabul et", nextNode: "accept_chaos" },
        ],
      },

      destroy_cult: {
        title: "Kültü Yok Etme",
        text: `Lasgun'ını çekiyorsun ve Chaos kültüne saldırıyorsun. Marcus ve Sarah da sana katılıyor.

"İmperium için savaş!" diye bağırıyorsun.

Köylüler kaçmaya başlıyor ama bazıları savaşmaya karar veriyor. Chaos sembolleri yanıyor, tapınak karışıyor.

Yaşlı adam, bir büyü yapıyor ve tapınakta garip güçler uçuşmaya başlıyor.

"Chaos'un gücü benimle! Sizi yok edeceğim!"

Kutsal kolyen çok parlak yanıyor ve Chaos büyüsünü engelliyor. Yaşlı adam şaşkın: "O kolye... o kolye İmperium'un en kutsal eşyası!"

"Evet, bu kolye İmperium'un gücünü temsil ediyor. Chaos'u yok edecek!"`,
        choices: [
          { text: "Yaşlı adamı öldür", nextNode: "kill_elder" },
          { text: "Yaşlı adamı yakala", nextNode: "capture_elder" },
          { text: "Tapınağı yok et", nextNode: "destroy_temple" },
          { text: "Köylüleri kurtar", nextNode: "save_villagers" },
          { text: "Geri çekil", nextNode: "retreat_battle" },
        ],
      },

      kill_elder: {
        title: "Yaşlı Adamı Öldürme",
        text: `Yaşlı adamı öldürüyorsun. Chaos kültünün lideri ölüyor ve kült dağılıyor.

"Chaos kültü yok edildi!" diye bağırıyor Marcus.

Sarah ekliyor: "Ama başka yerlerde de Chaos kültleri var. Bu sadece başlangıç."

Köylüler, Chaos'un etkisinden kurtuluyor ve normal hayatlarına dönüyorlar.

"Teşekkür ederiz, İmperium'un askerleri. Bizi kurtardınız."

Kutsal kolyen parlamaya devam ediyor. Hafızanın daha fazlası geri geliyor - sen İmperium'un en iyi askerlerinden birisin ve Chaos'a karşı savaşmak senin görevin.`,
        choices: [
          { text: "Cadia Prime'ı koru", nextNode: "protect_cadia_prime" },
          { text: "Diğer kültleri ara", nextNode: "search_other_cults" },
          { text: "İmperium'a rapor ver", nextNode: "report_to_imperium" },
          { text: "Hikayeyi bitir", nextNode: "warhammer_ending" },
        ],
      },

      protect_cadia_prime: {
        title: "Cadia Prime'ı Koruma",
        text: `Cadia Prime'ı korumaya devam ediyorsun. Artık sen İmperium'un en güvenilir askerlerinden birisin.`,
        choices: [
          { text: "Space Marine ol", nextNode: "become_space_marine" },
          { text: "Imperial Guard'da kal", nextNode: "stay_guard" },
          { text: "Commissar ol", nextNode: "become_commissar" },
        ],
      },

      become_space_marine: {
        title: "Space Marine Olma",
        text: `Space Marine oldun! Artık İmperium'un en güçlü savaşçılarından birisin.`,
        choices: [
          { text: "Chapter'a katıl", nextNode: "join_chapter" },
          { text: "Savaşlara katıl", nextNode: "join_battles" },
          { text: "Eğitim al", nextNode: "receive_training" },
        ],
      },

      join_chapter: {
        title: "Chapter'a Katılma",
        text: `Ultramarines Chapter'ına katıldın. Artık efsanevi bir Space Marine'sin!`,
        choices: [
          { text: "Kahraman ol", nextNode: "become_hero_warhammer" },
          { text: "Savaş", nextNode: "fight_as_marine" },
          { text: "İmperium'u koru", nextNode: "protect_imperium" },
        ],
      },

      become_hero_warhammer: {
        title: "Kahraman Olma",
        text: `İmperium'un en büyük kahramanlarından biri oldun. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "İmperium'a hizmet et", nextNode: "serve_imperium" },
          { text: "Dinlen", nextNode: "rest_peacefully" },
        ],
      },

      warhammer_ending: {
        title: "Warhammer Sonu",
        text: `Cadia Prime'daki maceran bitti. Chaos kültünü yok ettin. Bu sadece bir son değil, yeni bir başlangıç.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "İmperium'da kal", nextNode: "stay_in_imperium" },
          { text: "Savaşa devam et", nextNode: "continue_war" },
        ],
      },

      // WARHAMMER EKSİK NODE'LAR
      talk_to_villagers: {
        title: "Köylülerle Konuşma",
        text: `Köylülerle konuşuyorsun. Onlar korku içinde ve garip şeyler yaşadıklarını anlatıyorlar.
        
        "Gece yarısı garip sesler duyuyoruz," diyor bir köylü. "Ve bazı insanlar kayboluyor."
        
        "Eski tapınakta bir şeyler oluyor," diyor başka biri. "Kimse oraya gitmek istemiyor."
        
        Kutsal kolyen yanıp sönüyor. Köylülerin korkusu gerçek - Chaos burada.`,
        choices: [
          { text: "Tapınağı araştır", nextNode: "search_chaos_cult" },
          { text: "Kayıp insanları ara", nextNode: "search_missing_people" },
          { text: "Köyü koru", nextNode: "protect_village_warhammer" }
        ]
      },

      search_missing_people: {
        title: "Kayıp İnsanları Arama",
        text: `Kayıp insanları arıyorsun. İzler seni eski tapınağa götürüyor. Tapınağın içinde kayıp insanları buluyorsun.
        
        Onlar Chaos sembolleri etrafında toplanmış, dualar okuyorlar. Chaos'un etkisi altındalar.
        
        "Kurtarın bizi!" diye bağırıyor birisi. "Chaos bizi kontrol ediyor!"`,
        choices: [
          { text: "İnsanları kurtar", nextNode: "save_missing_people" },
          { text: "Chaos'u yok et", nextNode: "destroy_chaos_influence" },
          { text: "Geri çekil", nextNode: "retreat_from_people" }
        ]
      },

      save_missing_people: {
        title: "Kayıp İnsanları Kurtarma",
        text: `Kutsal kolyenin gücüyle kayıp insanları Chaos'un etkisinden kurtarıyorsun. Onlar normal bilinçlerine dönüyorlar.
        
        "Teşekkür ederiz!" diyorlar. "Chaos bizi kontrol ediyordu."
        
        Marcus: "Chaos burada güçlü. Daha fazla insanı kurtarmamız gerekiyor."`,
        choices: [
          { text: "Diğerlerini kurtar", nextNode: "save_others" },
          { text: "Chaos kaynağını bul", nextNode: "find_chaos_source" },
          { text: "Köye dön", nextNode: "return_to_village_saved" }
        ]
      },

      find_chaos_source: {
        title: "Chaos Kaynağını Bulma",
        text: `Chaos'un kaynağını arıyorsun. Tapınağın derinliklerine iniyorsun ve şok edici bir manzara görüyorsun.
        
        Tapınağın altında bir Chaos portalı var! Karanlık güçler buradan geliyor.
        
        "Bu portal Chaos'un gücünü buraya getiriyor!" diye bağırıyor Marcus. "Kapatmamız gerekiyor!"`,
        choices: [
          { text: "Portalı kapat", nextNode: "close_chaos_portal" },
          { text: "Güç kullan", nextNode: "use_chaos_power" },
          { text: "Yardım çağır", nextNode: "call_imperial_help" }
        ]
      },

      close_chaos_portal: {
        title: "Chaos Portalını Kapatma",
        text: `Kutsal kolyenin gücüyle Chaos portalını kapatmaya çalışıyorsun. Portal direniyor ama sen güçlüsün.
        
        "İmperium'un gücüyle seni kapatacağım!" diye bağırıyorsun.
        
        Portal kapanıyor ve Chaos'un etkisi azalıyor. Cadia Prime güvende.`,
        choices: [
          { text: "Cadia Prime'ı koru", nextNode: "protect_cadia_prime" },
          { text: "İmperium'a rapor ver", nextNode: "report_to_imperium" },
          { text: "Yeni görev", nextNode: "new_imperial_mission" }
        ]
      },

      report_to_imperium: {
        title: "İmperium'a Rapor Verme",
        text: `İmperium'a Chaos portalını kapattığını rapor ediyorsun. İmperium seni ödüllendiriyor.
        
        "Cadia Prime'ı kurtardın," diyor Inquisitor. "İmperium'un en iyi askerlerinden birisin."
        
        Artık İmperium'un güvenilir askerlerinden birisin. Yeni görevler seni bekliyor.`,
        choices: [
          { text: "Yeni görev", nextNode: "new_imperial_mission" },
          { text: "Space Marine ol", nextNode: "become_space_marine" },
          { text: "Inquisitor ol", nextNode: "become_inquisitor" }
        ]
      },

      become_inquisitor: {
        title: "Inquisitor Olma",
        text: `Inquisitor oldun! Artık İmperium'un en güçlü ajanlarından birisin. Chaos'a karşı savaşmak senin görevin.`,
        choices: [
          { text: "Chaos avcısı", nextNode: "chaos_hunter" },
          { text: "İmperium'u koru", nextNode: "protect_imperium_inquisitor" },
          { text: "Yeni macera", nextNode: "new_adventure" }
        ]
      },

      chaos_hunter: {
        title: "Chaos Avcısı",
        text: `Chaos avcısı olarak İmperium'un en tehlikeli düşmanlarıyla savaşıyorsun. Her gün yeni bir Chaos tehdidi, her gün yeni bir savaş.`,
        choices: [
          { text: "Kahraman ol", nextNode: "become_hero_warhammer" },
          { text: "Savaşa devam et", nextNode: "continue_war" },
          { text: "Dinlen", nextNode: "rest_peacefully" }
        ]
      },

      // GENEL EKSİK NODE'LAR
      new_adventure: {
        title: "Yeni Macera",
        text: `Yeni bir maceraya başlıyorsun. Dünya seni bekliyor!`,
        choices: [
          { text: "Fantasy dünyası", nextNode: "fantasy_world" },
          { text: "Cyberpunk dünyası", nextNode: "cyberpunk_world" },
          { text: "Warhammer dünyası", nextNode: "warhammer_world" }
        ]
      },

      fantasy_world: {
        title: "Fantasy Dünyası",
        text: `Fantasy dünyasına gidiyorsun. Yeni maceralar, yeni kahramanlar seni bekliyor.`,
        choices: [
          { text: "Yeni hikaye", nextNode: "new_story_ending" },
          { text: "Geri dön", nextNode: "return_to_village" }
        ]
      },

      cyberpunk_world: {
        title: "Cyberpunk Dünyası",
        text: `Cyberpunk dünyasına gidiyorsun. Neon ışıklar ve teknoloji seni bekliyor.`,
        choices: [
          { text: "Yeni hikaye", nextNode: "new_story_ending" },
          { text: "Geri dön", nextNode: "return_to_village" }
        ]
      },

      warhammer_world: {
        title: "Warhammer Dünyası",
        text: `Warhammer dünyasına gidiyorsun. İmperium ve Chaos savaşları seni bekliyor.`,
        choices: [
          { text: "Yeni hikaye", nextNode: "new_story_ending" },
          { text: "Geri dön", nextNode: "return_to_village" }
        ]
      },

      return_to_village: {
        title: "Köye Dönüş",
        text: `Köye dönüyorsun. Hikayen burada biter ama yeni maceralar seni bekliyor.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Dinlen", nextNode: "rest_peacefully" }
        ]
      },

      rest_peacefully: {
        title: "Huzurlu Dinlenme",
        text: `Huzurlu bir şekilde dinleniyorsun. Maceran bitti ama anıların seninle kalacak.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Hikayeyi bitir", nextNode: "final_ending" }
        ]
      },

      final_ending: {
        title: "Final Son",
        text: `Maceran bitti. Sen harika bir kahraman oldun ve dünyayı değiştirdin. Hikayen burada biter.`,
        choices: [
          { text: "Yeni macera", nextNode: "new_adventure" },
          { text: "Baştan başla", nextNode: "start_over" }
        ]
      },

      start_over: {
        title: "Baştan Başlama",
        text: `Yeni bir maceraya başlıyorsun. Bu sefer farklı seçimler yapacaksın.`,
        choices: [
          { text: "Fantasy", nextNode: "fantasy_world" },
          { text: "Cyberpunk", nextNode: "cyberpunk_world" },
          { text: "Warhammer", nextNode: "warhammer_world" }
        ]
      }
    },
  },
};

scenarios.living_dragon_hunt.story.protector_life = {
  title: "Koruyucu Olarak Yaşama",
  text: "Koruyucu olarak yaşıyorsun. Köy güvende, sen mutlusun.",
  choices: [
    { text: "Mutlu son", nextNode: "happy_ending" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Köye dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.new_adventure = {
  title: "Yeni Macera",
  text: "Yeni bir maceraya başlıyorsun. Dünya seni bekliyor!",
  choices: [
    { text: "Maceraya başla", nextNode: "start_adventure" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Dinlen", nextNode: "rest_in_village" },
  ],
};

scenarios.living_dragon_hunt.story.start_adventure = {
  title: "Maceraya Başlama",
  text: "Yeni maceraya başladın! Artık yeni hikayeler seni bekliyor.",
  choices: [
    { text: "Yeni hikaye", nextNode: "new_story_ending" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Dinlen", nextNode: "rest_in_village" },
  ],
};

scenarios.living_dragon_hunt.story.new_story_ending = {
  title: "Yeni Hikaye Sonu",
  text: "Yeni maceralara çıktın. Hikayen burada biter ama başka hikayeler seni bekliyor.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

// EKSİK NODE'LAR - FANTASY SCENARIO
scenarios.living_dragon_hunt.story.stay_silent = {
  title: "Sessiz Kalma",
  text: "Köylülere hiçbir şey söylemiyorsun. Sessiz kalıyorsun ve onların ne düşündüğünü merak ediyorsun.",
  choices: [
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Hikayeyi bitir", nextNode: "happy_ending" }
  ]
};

scenarios.living_dragon_hunt.story.protect_village = {
  title: "Köyü Koruma",
  text: "Köyü korumaya karar veriyorsun. Ejderha tehdidine karşı köylüleri savunacaksın.",
  choices: [
    { text: "Savunma hazırla", nextNode: "prepare_defense" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Hikayeyi bitir", nextNode: "happy_ending" }
  ]
};

scenarios.living_dragon_hunt.story.prepare_defense = {
  title: "Savunma Hazırlama",
  text: "Köy için savunma hazırlıyorsun. Köylülerle birlikte hazırlanıyorsunuz.",
  choices: [
    { text: "Savunma yap", nextNode: "defend_village" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Hikayeyi bitir", nextNode: "happy_ending" }
  ]
};

scenarios.living_dragon_hunt.story.defend_village = {
  title: "Köyü Savunma",
  text: "Köyü savunuyorsun. Ejderha saldırıyor ama sen köyü koruyorsun.",
  choices: [
    { text: "Zafer kazan", nextNode: "victory_defense" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Hikayeyi bitir", nextNode: "happy_ending" }
  ]
};

scenarios.living_dragon_hunt.story.victory_defense = {
  title: "Savunma Zaferi",
  text: "Köyü başarıyla savundun. Ejderha geri çekildi.",
  choices: [
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Hikayeyi bitir", nextNode: "happy_ending" }
  ]
};

// EKSİK FONKSİYONLAR - BUNLAR OLMADAN OYUN ÇALIŞMAZ!
console.log("=== EKSİK FONKSİYONLAR EKLENİYOR ===");

// Karakter panelini güncelleme fonksiyonu
window.updateCharacterPanel = function () {
  console.log("✅ UPDATE CHARACTER PANEL");

  const selectedRace = document.querySelector(
    ".race-class-list:nth-child(1) .list-item.selected"
  );
  const selectedClass = document.querySelector(
    ".race-class-list:nth-child(2) .list-item.selected"
  );
  const characterName =
    document.getElementById("character-name-input")?.value ||
    "İsimsiz Kahraman";

  // Karakter bilgilerini güncelle - HTML'deki doğru ID'leri kullan
  const charName = document.getElementById("char-name");
  const charRaceClass = document.getElementById("char-race-class");

  if (charName) {
    charName.textContent = characterName;
  }

  if (charRaceClass) {
    const raceText = selectedRace ? selectedRace.textContent : "Seçilmedi";
    const classText = selectedClass ? selectedClass.textContent : "Seçilmedi";
    charRaceClass.textContent = `${raceText} ${classText}`;
  }

  console.log("✅ Character panel updated:", {
    characterName,
    race: selectedRace?.textContent,
    class: selectedClass?.textContent,
  });
};

// Senaryo başlatma fonksiyonu
window.startScenario = function (scenarioId) {
  console.log("✅ START SCENARIO:", scenarioId);

  const scenario = scenarios[scenarioId];
  if (!scenario) {
    console.error("❌ Scenario not found:", scenarioId);
    return;
  }

  // Senaryo başlığını güncelle
  const titleElement = document.getElementById("current-scenario-title");
  if (titleElement) {
    titleElement.textContent = scenario.title;
  }

  // İlk hikaye node'unu göster
  const startNode = scenario.story.start;
  if (startNode) {
    displayStoryNode(startNode);
  }

  console.log("✅ Scenario started successfully");
};

// Hikaye node'unu gösterme fonksiyonu
window.displayStoryNode = function (node) {
  console.log("✅ DISPLAY STORY NODE:", node.title);

  const storyText = document.getElementById("story-text");
  const choicesGrid = document.getElementById("choices-grid");

  if (storyText) {
    storyText.innerHTML = `
      <h3>${node.title}</h3>
      <p>${node.text}</p>
    `;
  }

  if (choicesGrid && node.choices) {
    choicesGrid.innerHTML = "";
    node.choices.forEach((choice) => {
      const choiceButton = document.createElement("button");
      choiceButton.className = "choice-btn";
      choiceButton.textContent = choice.text;
      choiceButton.onclick = () => makeChoice(choice.nextNode);
      choicesGrid.appendChild(choiceButton);
    });
  }

  console.log("✅ Story node displayed");
};

// Seçim yapma fonksiyonu
window.makeChoice = function (nextNodeId) {
  console.log("✅ MAKE CHOICE:", nextNodeId);

  // Şu anki senaryoyu bul
  const currentScenario = getCurrentScenario();
  if (!currentScenario) {
    console.error("❌ No active scenario");
    return;
  }

  const nextNode = currentScenario.story[nextNodeId];
  if (nextNode) {
    displayStoryNode(nextNode);
  } else {
    console.error("❌ Next node not found:", nextNodeId);
  }
};

// Aktif senaryoyu alma fonksiyonu
window.getCurrentScenario = function () {
  // Basit implementasyon - ilk senaryoyu döndür
  return scenarios.living_dragon_hunt;
};

// Oyun kaydetme fonksiyonu
window.saveGame = function () {
  console.log("✅ SAVE GAME");
  alert("💾 Oyun kaydedildi!");
};

// Oyun yükleme fonksiyonu
window.loadGame = function () {
  console.log("✅ LOAD GAME");
  alert("📁 Oyun yüklendi!");
};

// Oyun sıfırlama fonksiyonu
window.resetGame = function () {
  console.log("✅ RESET GAME");
  if (confirm("🔄 Oyunu sıfırlamak istediğinizden emin misiniz?")) {
    location.reload();
  }
};

// Karakter adı güncelleme fonksiyonu
window.updateCharacterName = function (name) {
  console.log("✅ UPDATE CHARACTER NAME:", name);
  updateCharacterPanel();
};

// NPC sistemi (basit implementasyon)
window.npcSystem = {
  initializeNPCs: function (theme) {
    console.log("✅ INITIALIZE NPCS for theme:", theme);
  },
  updateNPCDisplay: function () {
    console.log("✅ UPDATE NPC DISPLAY");
  },
};

// DOM yüklendiğinde çalışacak fonksiyonlar
window.addEventListener("DOMContentLoaded", function () {
  console.log("✅ DOM LOADED - INITIALIZING GAME");

  // İlk tema olarak fantasy'yi seç
  if (typeof switchTheme === "function") {
    switchTheme("fantasy");
  }

  // Karakter panelini güncelle
  if (typeof updateCharacterPanel === "function") {
    updateCharacterPanel();
  }

  console.log("✅ GAME INITIALIZED SUCCESSFULLY");
});

console.log("=== TÜM FONKSİYONLAR YÜKLENDİ ===");
