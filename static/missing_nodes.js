// EKSİK NODE'LAR - TÜM SENARYOLAR İÇİN

// SCENARIOS OBJESİNİ TANIMLA
if (typeof scenarios === "undefined") {
  window.scenarios = {};
}

// WARHAMMER EKSİK NODE'LAR
scenarios.warhammer_imperial_crisis.story.recover_memory_warhammer = {
  title: "Hafızayı Geri Getirme",
  text: `Kutsal kolyenin gücüyle hafızanı geri getirmeye çalışıyorsun. Anılar geliyor...
  
  Sen Cadian Shock Troops'un en iyi askerlerinden birisin. Chaos'a karşı savaşmak senin görevin. Bu köyde Chaos kültü var ve sen onları durdurmak için buradasın.
  
  "Hafızam geri geldi!" diye bağırıyorsun. "Chaos kültünü durdurmam gerekiyor!"`,
  choices: [
    { text: "Chaos kültünü ara", nextNode: "search_chaos_cult" },
    { text: "Köylülerle konuş", nextNode: "talk_to_villagers" },
    { text: "Kolyeyi kullan", nextNode: "use_necklace_power" },
  ],
};

scenarios.warhammer_imperial_crisis.story.examine_necklace_warhammer = {
  title: "Kolyeyi İnceleme",
  text: `Kutsal kolyeyi inceliyorsun. Üzerinde İmperium'un en kutsal sembolleri var. Bu kolye Chaos'a karşı güçlü bir silah.
  
  Kolye yanıp sönüyor ve seni Chaos'un kaynağına doğru yönlendiriyor.
  
  "Bu kolye Chaos'u bulmama yardım edecek!" diyorsun.`,
  choices: [
    { text: "Kolyeyi kullan", nextNode: "use_necklace_power" },
    { text: "Chaos'u ara", nextNode: "search_chaos_cult" },
    { text: "Köylülere göster", nextNode: "show_necklace_villagers" },
  ],
};

scenarios.warhammer_imperial_crisis.story.explore_village = {
  title: "Köyü Keşfetme",
  text: `Köyü keşfediyorsun. Garip izler, tuhaf semboller, gizli toplantı yerleri buluyorsun.
  
  Köylüler korku içinde ve bir şeylerden kaçıyorlar. Eski tapınağa doğru izler var.
  
  "Burada Chaos var," diyorsun. "Ve güçlü."`,
  choices: [
    { text: "Tapınağa git", nextNode: "search_chaos_cult" },
    { text: "Köylülerle konuş", nextNode: "talk_to_villagers" },
    { text: "İzleri takip et", nextNode: "follow_tracks" },
  ],
};

scenarios.warhammer_imperial_crisis.story.search_chaos_cult = {
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
};

scenarios.warhammer_imperial_crisis.story.talk_to_villagers = {
  title: "Köylülerle Konuşma",
  text: `Köylülerle konuşuyorsun. Onlar korku içinde ve garip şeyler yaşadıklarını anlatıyorlar.
  
  "Gece yarısı garip sesler duyuyoruz," diyor bir köylü. "Ve bazı insanlar kayboluyor."
  
  "Eski tapınakta bir şeyler oluyor," diyor başka biri. "Kimse oraya gitmek istemiyor."
  
  Kutsal kolyen yanıp sönüyor. Köylülerin korkusu gerçek - Chaos burada.`,
  choices: [
    { text: "Tapınağı araştır", nextNode: "search_chaos_cult" },
    { text: "Kayıp insanları ara", nextNode: "search_missing_people" },
    { text: "Köyü koru", nextNode: "protect_village_warhammer" },
  ],
};

// DAHA FAZLA WARHAMMER NODE'LARI
scenarios.warhammer_imperial_crisis.story.use_necklace_power = {
  title: "Kolye Gücünü Kullanma",
  text: `Kutsal kolyenin gücünü kullanıyorsun. Kolye parlak ışık saçıyor ve Chaos'un kaynağını gösteriyor.
  
  Eski tapınakta güçlü bir Chaos varlığı var. Kolye seni oraya yönlendiriyor.
  
  "Chaos'un kaynağını buldum!" diyorsun.`,
  choices: [
    { text: "Tapınağa git", nextNode: "search_chaos_cult" },
    { text: "Güç kullan", nextNode: "use_imperial_power" },
    { text: "Yardım çağır", nextNode: "call_imperial_help" },
  ],
};

scenarios.warhammer_imperial_crisis.story.show_necklace_villagers = {
  title: "Kolyeyi Köylülere Gösterme",
  text: `Kutsal kolyeyi köylülere gösteriyorsun. Onlar kolyenin gücünü görünce şaşkın kalıyorlar.
  
  "Bu İmperium'un kutsal eşyası!" diyor bir köylü. "Sen gerçekten İmperium'un seçilmişisin!"
  
  Köylüler artık sana güveniyor ve Chaos kültü hakkında bilgi veriyorlar.`,
  choices: [
    { text: "Bilgi al", nextNode: "get_villager_info" },
    { text: "Köylüleri koru", nextNode: "protect_villagers" },
    { text: "Chaos'u ara", nextNode: "search_chaos_cult" },
  ],
};

scenarios.warhammer_imperial_crisis.story.get_villager_info = {
  title: "Köylülerden Bilgi Alma",
  text: `Köylülerden Chaos kültü hakkında bilgi alıyorsun. Onlar korku içinde anlatıyorlar.
  
  "Gece yarısı eski tapınakta toplanıyorlar," diyor bir köylü. "Ve garip dualar okuyorlar."
  
  "Bazı insanlar kayboluyor ve geri dönmüyor," diyor başka biri. "Chaos onları alıyor."`,
  choices: [
    { text: "Tapınağa git", nextNode: "search_chaos_cult" },
    { text: "Kayıp insanları ara", nextNode: "search_missing_people" },
    { text: "Köyü koru", nextNode: "protect_village_warhammer" },
  ],
};

scenarios.warhammer_imperial_crisis.story.protect_village_warhammer = {
  title: "Köyü Koruma",
  text: `Köyü Chaos'tan korumaya karar veriyorsun. Kutsal kolyenin gücüyle köyün etrafında koruyucu bir alan oluşturuyorsun.
  
  "Köy artık güvende!" diyorsun. "Chaos buraya giremez!"
  
  Köylüler güvenli hissediyor ve sana teşekkür ediyorlar.`,
  choices: [
    { text: "Chaos'u ara", nextNode: "search_chaos_cult" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "İmperium'a rapor ver", nextNode: "report_to_imperium" },
  ],
};

scenarios.warhammer_imperial_crisis.story.stay_in_village = {
  title: "Köyde Kalma",
  text: `Köyde kalmaya karar veriyorsun. Köylüleri koruyorsun ve Chaos'a karşı savaşıyorsun.
  
  Artık sen köyün koruyucususun. İmperium'un buradaki temsilcisi.`,
  choices: [
    { text: "Koruyucu ol", nextNode: "become_village_protector" },
    { text: "Yeni görev", nextNode: "new_imperial_mission" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

scenarios.warhammer_imperial_crisis.story.become_village_protector = {
  title: "Köy Koruyucusu Olma",
  text: `Köyün koruyucusu oldun. Cadia Prime'ın bu köyünde Chaos'a karşı savaşıyorsun.
  
  Köylüler sana güveniyor ve sen onları koruyorsun. İmperium'un buradaki gücüsün.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero_warhammer" },
    { text: "Koruyucu kal", nextNode: "stay_protector" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.warhammer_imperial_crisis.story.stay_protector = {
  title: "Koruyucu Olarak Kalma",
  text: `Koruyucu olarak kalmaya karar veriyorsun. Köy güvende, sen mutlusun.
  
  Bu senin yeni evin. İmperium'un buradaki temsilcisi.`,
  choices: [
    { text: "Mutlu son", nextNode: "happy_ending_warhammer" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.warhammer_imperial_crisis.story.happy_ending_warhammer = {
  title: "Warhammer Mutlu Son",
  text: `Cadia Prime'da mutlu bir hayat yaşıyorsun. Köyü koruyorsun, Chaos'a karşı savaşıyorsun.
  
  İmperium'un en iyi askerlerinden birisin ve huzurlu bir hayat yaşıyorsun.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

// FANTASY EKSİK NODE'LAR
scenarios.living_dragon_hunt.story.track_dragon = {
  title: "Ejderhayı Takip Etme",
  text: `Ejderhanın izlerini takip ediyorsun. Büyük ayak izleri ve yanık toprak izleri seni dağlara doğru götürüyor.
  
  "Ejderha buradan geçmiş," diyorsun. "Ve yakın zamanda."
  
  İzler seni dağın derinliklerine götürüyor. Karanlık bir mağara görüyorsun.`,
  choices: [
    { text: "Mağaraya gir", nextNode: "enter_cave" },
    { text: "Gözetle", nextNode: "spy_on_dragon" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.enter_cave = {
  title: "Mağaraya Giriş",
  text: `Mağaraya giriyorsun. İçeride karanlık ve sıcak. Ejderhanın nefesini duyabiliyorsun.
  
  "Ejderha burada," diye fısıldıyorsun. "Dikkatli olmalıyım."
  
  Mağaranın derinliklerinde kırmızı ışık görüyorsun. Ejderha orada.`,
  choices: [
    { text: "Ejderhaya yaklaş", nextNode: "approach_dragon" },
    { text: "Gözetle", nextNode: "spy_on_dragon" },
    { text: "Geri çekil", nextNode: "retreat_from_cave" },
  ],
};

scenarios.living_dragon_hunt.story.approach_dragon = {
  title: "Ejderhaya Yaklaşma",
  text: `Ejderhaya yaklaşıyorsun. Büyük kırmızı ejderha seni görüyor ama saldırmıyor.
  
  "Sen kimsin?" diye soruyor ejderha. "Neden buradasın?"
  
  Ejderha beklenmedik şekilde konuşuyor. Bu şaşırtıcı.`,
  choices: [
    { text: "Barış teklif et", nextNode: "offer_peace" },
    { text: "Saldır", nextNode: "attack_dragon" },
    { text: "Konuş", nextNode: "talk_to_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.offer_peace = {
  title: "Barış Teklif Etme",
  text: `Ejderhaya barış teklif ediyorsun. "Köyü yakmayı bırak, sana yardım edelim."
  
  Ejderha düşünüyor. "Köylüler beni korkutuyor. Ama sen farklısın."
  
  "Barış yapalım," diyor ejderha. "Ama köylüler kabul etmeli."`,
  choices: [
    { text: "Köylüleri ikna et", nextNode: "convince_villagers" },
    { text: "Barış anlaşması yap", nextNode: "make_peace_deal" },
    { text: "Ejderhayı koru", nextNode: "protect_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.make_peace_deal = {
  title: "Barış Anlaşması Yapma",
  text: `Ejderha ile barış anlaşması yapıyorsun. Artık köy güvende.
  
  "Barış sağlandı!" diye bağırıyorsun.
  
  Köylüler şaşkın ama mutlu. Ejderha artık dost.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.protect_dragon = {
  title: "Ejderhayı Koruma",
  text: `Ejderhayı korumaya karar veriyorsun. Köylülerden onu koruyorsun.
  
  "Ejderha dostumuz!" diye bağırıyorsun.
  
  Köylüler şaşkın ama seni dinliyorlar.`,
  choices: [
    { text: "Koruyucu ol", nextNode: "become_protector" },
    { text: "Barış sağla", nextNode: "make_peace_deal" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.become_protector = {
  title: "Koruyucu Olma",
  text: `Köyün koruyucusu oldun. Ejderhayı ve köylüleri koruyorsun.
  
  "Ben koruyucu olacağım!" diyorsun.
  
  Artık hem ejderha hem köylüler sana güveniyor.`,
  choices: [
    { text: "Mutlu son", nextNode: "happy_ending" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
  ],
};

scenarios.living_dragon_hunt.story.happy_ending = {
  title: "Mutlu Son",
  text: `Köyde mutlu bir hayat yaşıyorsun. Ejderha dostun, köylüler sana güveniyor.
  
  "Bu benim evim," diyorsun. "Ve mutluyum."
  
  Hikayen burada biter ama anıların seninle kalacak.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

scenarios.living_dragon_hunt.story.rest_peacefully = {
  title: "Huzurlu Dinlenme",
  text: `Huzurlu bir şekilde dinleniyorsun. Maceran bitti ama anıların seninle kalacak.
  
  "Güzel bir maceraydı," diyorsun.
  
  Artık dinlenme zamanı.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Hikayeyi bitir", nextNode: "final_ending" },
  ],
};

scenarios.living_dragon_hunt.story.final_ending = {
  title: "Final Son",
  text: `Maceran bitti. Sen harika bir kahraman oldun ve dünyayı değiştirdin. Hikayen burada biter.
  
  "Teşekkürler," diyorsun. "Bu harika bir maceraydı."
  
  Artık yeni maceralar seni bekliyor.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Baştan başla", nextNode: "start_over" },
  ],
};

scenarios.living_dragon_hunt.story.start_over = {
  title: "Baştan Başlama",
  text: `Yeni bir maceraya başlıyorsun. Bu sefer farklı seçimler yapacaksın.
  
  "Yeni bir başlangıç," diyorsun.
  
  Dünya seni bekliyor.`,
  choices: [
    { text: "Fantasy", nextNode: "fantasy_world" },
    { text: "Cyberpunk", nextNode: "cyberpunk_world" },
    { text: "Warhammer", nextNode: "warhammer_world" },
  ],
};

// CYBERPUNK EKSİK NODE'LAR
scenarios.cyberpunk_hive_city.story.hack_system = {
  title: "Sistemi Hack Etme",
  text: `Sistemi hack etmeye çalışıyorsun. Neural implant'ın ile sisteme bağlanıyorsun.
  
  "Sisteme giriyorum," diyorsun. "Dikkatli olmalıyım."
  
  Sistem karmaşık ama sen güçlüsün. Hack başarılı.`,
  choices: [
    { text: "Veri çal", nextNode: "steal_data" },
    { text: "Sistemi boz", nextNode: "corrupt_system" },
    { text: "Geri çekil", nextNode: "retreat_from_hack" },
  ],
};

scenarios.cyberpunk_hive_city.story.steal_data = {
  title: "Veri Çalma",
  text: `Önemli verileri çalıyorsun. Şirketin sırları artık senin elinde.
  
  "Veriler çalındı!" diye bağırıyorsun.
  
  Artık şirkete karşı güçlü bir silahın var.`,
  choices: [
    { text: "Şirketi tehdit et", nextNode: "threaten_corporation" },
    { text: "Verileri sat", nextNode: "sell_data" },
    { text: "Verileri yayınla", nextNode: "publish_data" },
  ],
};

scenarios.cyberpunk_hive_city.story.threaten_corporation = {
  title: "Şirketi Tehdit Etme",
  text: `Şirketi tehdit ediyorsun. Verileri kullanarak onları zorluyorsun.
  
  "Verileri yayınlayacağım!" diye tehdit ediyorsun.
  
  Şirket korkuyor ve senin isteklerini kabul ediyor.`,
  choices: [
    { text: "Şirketi kontrol et", nextNode: "control_corporation" },
    { text: "Zengin ol", nextNode: "become_rich" },
    { text: "Sistemi değiştir", nextNode: "change_system" },
  ],
};

scenarios.cyberpunk_hive_city.story.control_corporation = {
  title: "Şirketi Kontrol Etme",
  text: `Şirketi kontrol etmeye başlıyorsun. Artık güçlü bir pozisyondasın.
  
  "Şirket artık benim!" diyorsun.
  
  Artık Hive City'nin en güçlü insanlarından birisin.`,
  choices: [
    { text: "Güçlü lider ol", nextNode: "become_powerful_leader" },
    { text: "Sistemi değiştir", nextNode: "change_system" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.become_powerful_leader = {
  title: "Güçlü Lider Olma",
  text: `Hive City'nin en güçlü liderlerinden biri oldun. Şirketler seni korkuyor.
  
  "Artık ben güçlüyüm!" diyorsun.
  
  Hive City'de yeni bir düzen kuruyorsun.`,
  choices: [
    { text: "Mutlu son", nextNode: "happy_ending" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

// GENEL EKSİK NODE'LAR
scenarios.living_dragon_hunt.story.new_adventure = {
  title: "Yeni Macera",
  text: `Yeni bir maceraya başlıyorsun. Dünya seni bekliyor!`,
  choices: [
    { text: "Fantasy dünyası", nextNode: "fantasy_world" },
    { text: "Cyberpunk dünyası", nextNode: "cyberpunk_world" },
    { text: "Warhammer dünyası", nextNode: "warhammer_world" },
  ],
};

scenarios.living_dragon_hunt.story.fantasy_world = {
  title: "Fantasy Dünyası",
  text: `Fantasy dünyasına gidiyorsun. Yeni maceralar, yeni kahramanlar seni bekliyor.`,
  choices: [
    { text: "Yeni hikaye", nextNode: "new_story_ending" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.cyberpunk_world = {
  title: "Cyberpunk Dünyası",
  text: `Cyberpunk dünyasına gidiyorsun. Neon ışıklar ve teknoloji seni bekliyor.`,
  choices: [
    { text: "Yeni hikaye", nextNode: "new_story_ending" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.warhammer_world = {
  title: "Warhammer Dünyası",
  text: `Warhammer dünyasına gidiyorsun. İmperium ve Chaos savaşları seni bekliyor.`,
  choices: [
    { text: "Yeni hikaye", nextNode: "new_story_ending" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.return_to_village = {
  title: "Köye Dönüş",
  text: `Köye dönüyorsun. Hikayen burada biter ama yeni maceralar seni bekliyor.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

scenarios.living_dragon_hunt.story.new_story_ending = {
  title: "Yeni Hikaye Sonu",
  text: `Yeni maceralara çıktın. Hikayen burada biter ama başka hikayeler seni bekliyor.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

// DAHA FAZLA EKSİK NODE'LAR - TÜM SENARYOLAR İÇİN

// FANTASY EKSİK NODE'LAR - DEVAMI
scenarios.living_dragon_hunt.story.spy_on_dragon = {
  title: "Ejderhayı Gözetleme",
  text: `Ejderhayı gizlice gözetliyorsun. Büyük kırmızı ejderha mağaranın girişinde oturuyor ve etrafı izliyor.`,
  choices: [
    { text: "Yaklaş", nextNode: "approach_dragon" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.return_to_village = {
  title: "Köye Dönüş",
  text: `Köye dönüyorsun. Köylüler seni merakla bekliyor.`,
  choices: [
    { text: "Bilgi ver", nextNode: "report_to_villagers" },
    { text: "Yardım iste", nextNode: "ask_for_help" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.build_barricades = {
  title: "Barikat Kurma",
  text: `Köylülerle birlikte barikatlar kuruyorsunuz. Ejderhaya karşı savunma hazırlıyorsunuz.`,
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Daha fazla hazırlık", nextNode: "more_preparation" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.prepare_weapons = {
  title: "Silah Hazırlama",
  text: `Köylülerle birlikte silahlar hazırlıyorsunuz. Oklar, mızraklar, kılıçlar.`,
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Daha fazla silah", nextNode: "more_weapons" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.plan_strategy = {
  title: "Strateji Planlama",
  text: `Köylülerle birlikte ejderhaya karşı strateji planlıyorsunuz.`,
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Tuzak kur", nextNode: "set_trap" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.go_to_city = {
  title: "Şehre Gitme",
  text: `Yakındaki şehre gidiyorsun. Askerler çağırmak için.`,
  choices: [
    { text: "Askerler çağır", nextNode: "call_soldiers" },
    { text: "Kahraman ara", nextNode: "find_hero" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.find_wizard = {
  title: "Büyücü Arama",
  text: `Yakındaki ormanda büyücü arıyorsun. Ejderhaya karşı büyü gerekli.`,
  choices: [
    { text: "Büyücüyü bul", nextNode: "find_wizard_success" },
    { text: "Başka yerde ara", nextNode: "search_elsewhere" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.find_hero = {
  title: "Kahraman Arama",
  text: `Yakındaki kasabalarda kahraman arıyorsun. Ejderha avcısı gerekli.`,
  choices: [
    { text: "Kahramanı bul", nextNode: "find_hero_success" },
    { text: "Başka yerde ara", nextNode: "search_elsewhere" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.flee_to_city = {
  title: "Şehre Kaçma",
  text: `Korkuya yenik düşüyorsun ve şehre kaçıyorsun.`,
  choices: [
    { text: "Şehirde kal", nextNode: "stay_in_city" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Yeni hayat", nextNode: "new_life" },
  ],
};

scenarios.living_dragon_hunt.story.flee_to_forest = {
  title: "Ormana Kaçma",
  text: `Korkuya yenik düşüyorsun ve ormana kaçıyorsun.`,
  choices: [
    { text: "Ormanda kal", nextNode: "stay_in_forest" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Yeni hayat", nextNode: "new_life" },
  ],
};

// WARHAMMER EKSİK NODE'LAR - DEVAMI
scenarios.warhammer_imperial_crisis.story.seek_help_warhammer = {
  title: "Yardım Arama",
  text: `İmperium'dan yardım arıyorsun. Space Marine'lar gerekli.`,
  choices: [
    { text: "Space Marine çağır", nextNode: "call_space_marines" },
    { text: "İmperial Guard çağır", nextNode: "call_imperial_guard" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.follow_tracks = {
  title: "İzleri Takip Etme",
  text: `Garip izleri takip ediyorsun. Chaos'un izleri.`,
  choices: [
    { text: "Tapınağa git", nextNode: "search_chaos_cult" },
    { text: "Gözetle", nextNode: "spy_on_cult" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.enter_temple = {
  title: "Tapınağa Giriş",
  text: `Tapınağa giriyorsun. İçeride Chaos kültü üyeleri var.`,
  choices: [
    { text: "Savaş", nextNode: "fight_cult" },
    { text: "Gözetle", nextNode: "spy_on_cult" },
    { text: "Geri çekil", nextNode: "retreat_from_temple" },
  ],
};

scenarios.warhammer_imperial_crisis.story.retreat_from_temple = {
  title: "Tapınaktan Geri Çekilme",
  text: `Tapınaktan geri çekiliyorsun. Güçlü bir Chaos varlığı var.`,
  choices: [
    { text: "Yardım çağır", nextNode: "call_for_help" },
    { text: "Plan yap", nextNode: "make_plan_warhammer" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.spy_on_cult = {
  title: "Kültü Gözetleme",
  text: `Chaos kültünü gizlice gözetliyorsun. Güçlü bir varlık var.`,
  choices: [
    { text: "Saldır", nextNode: "attack_cult" },
    { text: "Plan yap", nextNode: "make_plan_warhammer" },
    { text: "Geri çekil", nextNode: "retreat_from_temple" },
  ],
};

scenarios.warhammer_imperial_crisis.story.call_for_help = {
  title: "Yardım Çağırma",
  text: `İmperium'dan yardım çağırıyorsun. Space Marine'lar geliyor.`,
  choices: [
    { text: "Savaşa katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.make_plan_warhammer = {
  title: "Plan Yapma",
  text: `Chaos'a karşı plan yapıyorsun. Kutsal kolyenin gücünü kullanacaksın.`,
  choices: [
    { text: "Saldır", nextNode: "attack_cult" },
    { text: "Tuzak kur", nextNode: "set_trap_warhammer" },
    { text: "Yardım bekle", nextNode: "wait_for_help" },
  ],
};

scenarios.warhammer_imperial_crisis.story.search_missing_people = {
  title: "Kayıp İnsanları Arama",
  text: `Kayıp insanları arıyorsun. Chaos onları almış.`,
  choices: [
    { text: "Tapınağa git", nextNode: "search_chaos_cult" },
    { text: "İzleri takip et", nextNode: "follow_tracks" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.protect_villagers = {
  title: "Köylüleri Koruma",
  text: `Köylüleri Chaos'tan koruyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Chaos'u ara", nextNode: "search_chaos_cult" },
    { text: "Yardım çağır", nextNode: "call_for_help" },
  ],
};

scenarios.warhammer_imperial_crisis.story.use_imperial_power = {
  title: "İmperial Güç Kullanma",
  text: `İmperium'un gücünü kullanıyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Chaos'u yok et", nextNode: "destroy_chaos" },
    { text: "Tapınağa git", nextNode: "search_chaos_cult" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.call_imperial_help = {
  title: "İmperial Yardım Çağırma",
  text: `İmperium'dan yardım çağırıyorsun. Space Marine'lar geliyor.`,
  choices: [
    { text: "Savaşa katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.report_to_imperium = {
  title: "İmperium'a Rapor Verme",
  text: `İmperium'a rapor veriyorsun. Chaos tehdidi hakkında bilgi veriyorsun.`,
  choices: [
    { text: "Yeni görev", nextNode: "new_imperial_mission" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

scenarios.warhammer_imperial_crisis.story.new_imperial_mission = {
  title: "Yeni İmperial Görev",
  text: `Yeni bir İmperial görev alıyorsun. Chaos'a karşı savaşmaya devam edeceksin.`,
  choices: [
    { text: "Görevi kabul et", nextNode: "accept_mission" },
    { text: "Reddet", nextNode: "reject_mission" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

scenarios.warhammer_imperial_crisis.story.become_hero_warhammer = {
  title: "Warhammer Kahramanı Olma",
  text: `İmperium'un kahramanı oldun. Chaos'a karşı savaşan en iyi askerlerden birisin.`,
  choices: [
    { text: "Mutlu son", nextNode: "happy_ending_warhammer" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

// CYBERPUNK EKSİK NODE'LAR - DEVAMI
scenarios.cyberpunk_hive_city.story.go_upstairs = {
  title: "Yukarı Çıkma",
  text: `Hive City'nin üst katmanlarına çıkıyorsun. Neon ışıklar ve teknoloji.`,
  choices: [
    { text: "Şirketi ara", nextNode: "find_corporation" },
    { text: "Veri ara", nextNode: "search_data" },
    { text: "Kaç", nextNode: "escape_hive" },
  ],
};

scenarios.cyberpunk_hive_city.story.search_data = {
  title: "Veri Arama",
  text: `Önemli veriler arıyorsun. Şirketin sırları burada.`,
  choices: [
    { text: "Veri bul", nextNode: "find_data" },
    { text: "Sistemi hack et", nextNode: "hack_system" },
    { text: "Kaç", nextNode: "escape_hive" },
  ],
};

scenarios.cyberpunk_hive_city.story.escape_hive = {
  title: "Hive'dan Kaçma",
  text: `Hive'dan kaçıyorsun. Tehlikeli bir yer.`,
  choices: [
    { text: "Güvenli yere git", nextNode: "go_to_safe_place" },
    { text: "Geri dön", nextNode: "return_to_hive" },
    { text: "Yeni hayat", nextNode: "new_life" },
  ],
};

scenarios.cyberpunk_hive_city.story.corrupt_system = {
  title: "Sistemi Bozma",
  text: `Sistemi bozuyorsun. Şirketin kontrolünü kaybetmesine neden oluyorsun.`,
  choices: [
    { text: "Kaos yarat", nextNode: "create_chaos" },
    { text: "Geri çekil", nextNode: "retreat_from_hack" },
    { text: "Veri çal", nextNode: "steal_data" },
  ],
};

scenarios.cyberpunk_hive_city.story.retreat_from_hack = {
  title: "Hack'ten Geri Çekilme",
  text: `Hack işleminden geri çekiliyorsun. Sistem çok güçlü.`,
  choices: [
    { text: "Yukarı çık", nextNode: "go_upstairs" },
    { text: "Veri ara", nextNode: "search_data" },
    { text: "Kaç", nextNode: "escape_hive" },
  ],
};

scenarios.cyberpunk_hive_city.story.sell_data = {
  title: "Veri Satma",
  text: `Çaldığın verileri satıyorsun. Zengin oluyorsun.`,
  choices: [
    { text: "Zengin ol", nextNode: "become_rich" },
    { text: "Şirketi tehdit et", nextNode: "threaten_corporation" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.publish_data = {
  title: "Veri Yayınlama",
  text: `Verileri yayınlıyorsun. Şirketin sırları ortaya çıkıyor.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Şirketi tehdit et", nextNode: "threaten_corporation" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.become_rich = {
  title: "Zengin Olma",
  text: `Zengin oldun. Hive City'de güçlü bir pozisyondasın.`,
  choices: [
    { text: "Güçlü lider ol", nextNode: "become_powerful_leader" },
    { text: "Şirketi kontrol et", nextNode: "control_corporation" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.change_system = {
  title: "Sistemi Değiştirme",
  text: `Hive City'nin sistemini değiştiriyorsun. Yeni bir düzen kuruyorsun.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Güçlü lider ol", nextNode: "become_powerful_leader" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.find_corporation = {
  title: "Şirketi Bulma",
  text: `Şirketi buluyorsun. Arasaka'nın merkezi.`,
  choices: [
    { text: "Sistemi hack et", nextNode: "hack_system" },
    { text: "Veri ara", nextNode: "search_data" },
    { text: "Kaç", nextNode: "escape_hive" },
  ],
};

scenarios.cyberpunk_hive_city.story.find_data = {
  title: "Veri Bulma",
  text: `Önemli verileri buluyorsun. Şirketin sırları senin elinde.`,
  choices: [
    { text: "Veri çal", nextNode: "steal_data" },
    { text: "Sistemi hack et", nextNode: "hack_system" },
    { text: "Kaç", nextNode: "escape_hive" },
  ],
};

scenarios.cyberpunk_hive_city.story.go_to_safe_place = {
  title: "Güvenli Yere Gitme",
  text: `Güvenli bir yere gidiyorsun. Hive City'nin dışında.`,
  choices: [
    { text: "Yeni hayat", nextNode: "new_life" },
    { text: "Geri dön", nextNode: "return_to_hive" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.return_to_hive = {
  title: "Hive'a Dönüş",
  text: `Hive'a geri dönüyorsun. Maceraya devam edeceksin.`,
  choices: [
    { text: "Sistemi hack et", nextNode: "hack_system" },
    { text: "Veri ara", nextNode: "search_data" },
    { text: "Yukarı çık", nextNode: "go_upstairs" },
  ],
};

scenarios.cyberpunk_hive_city.story.create_chaos = {
  title: "Kaos Yaratma",
  text: `Hive City'de kaos yaratıyorsun. Sistemler çöküyor.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Güçlü lider ol", nextNode: "become_powerful_leader" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.cyberpunk_hive_city.story.become_hero = {
  title: "Cyberpunk Kahramanı Olma",
  text: `Hive City'nin kahramanı oldun. Şirketlere karşı savaşan en iyi netrunner'lardan birisin.`,
  choices: [
    { text: "Mutlu son", nextNode: "happy_ending" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
  ],
};

// GENEL EKSİK NODE'LAR - DEVAMI
scenarios.living_dragon_hunt.story.report_to_villagers = {
  title: "Köylülere Rapor Verme",
  text: `Köylülere ejderha hakkında bilgi veriyorsun.`,
  choices: [
    { text: "Plan yap", nextNode: "make_plan" },
    { text: "Yardım iste", nextNode: "ask_for_help" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.ask_for_help = {
  title: "Yardım İsteme",
  text: `Köylülerden yardım istiyorsun. Ejderhaya karşı birlikte savaşacaksınız.`,
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Plan yap", nextNode: "make_plan" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.make_plan = {
  title: "Plan Yapma",
  text: `Ejderhaya karşı plan yapıyorsun. Köylülerle birlikte.`,
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Tuzak kur", nextNode: "set_trap" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.prepare_for_battle = {
  title: "Savaşa Hazırlanma",
  text: `Ejderhaya karşı savaşa hazırlanıyorsun. Köylülerle birlikte.`,
  choices: [
    { text: "Savaş", nextNode: "fight_dragon" },
    { text: "Daha fazla hazırlık", nextNode: "more_preparation" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.more_preparation = {
  title: "Daha Fazla Hazırlık",
  text: `Daha fazla hazırlık yapıyorsun. Ejderhaya karşı güçlü olmalısın.`,
  choices: [
    { text: "Savaş", nextNode: "fight_dragon" },
    { text: "Daha fazla silah", nextNode: "more_weapons" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
  ],
};

scenarios.living_dragon_hunt.story.wait_for_dragon = {
  title: "Ejderhayı Bekleme",
  text: `Ejderhayı bekliyorsun. Köylülerle birlikte hazırlıklısınız.`,
  choices: [
    { text: "Savaş", nextNode: "fight_dragon" },
    { text: "Daha fazla hazırlık", nextNode: "more_preparation" },
    { text: "Geri çekil", nextNode: "retreat_from_battle" },
  ],
};

scenarios.living_dragon_hunt.story.set_trap = {
  title: "Tuzak Kurma",
  text: `Ejderha için tuzak kuruyorsun. Köylülerle birlikte.`,
  choices: [
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.call_soldiers = {
  title: "Askerler Çağırma",
  text: `Şehirden askerler çağırıyorsun. Ejderhaya karşı güçlü bir ordu.`,
  choices: [
    { text: "Savaşa katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.find_wizard_success = {
  title: "Büyücüyü Bulma",
  text: `Büyücüyü buldun. Ejderhaya karşı güçlü bir müttefik.`,
  choices: [
    { text: "Büyücüyle savaş", nextNode: "fight_with_wizard" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.find_hero_success = {
  title: "Kahramanı Bulma",
  text: `Kahramanı buldun. Ejderha avcısı güçlü bir müttefik.`,
  choices: [
    { text: "Kahramanla savaş", nextNode: "fight_with_hero" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Plan yap", nextNode: "make_plan" },
  ],
};

scenarios.living_dragon_hunt.story.search_elsewhere = {
  title: "Başka Yerde Arama",
  text: `Başka yerlerde arama yapıyorsun. Yardım gerekli.`,
  choices: [
    { text: "Şehre git", nextNode: "go_to_city" },
    { text: "Büyücü ara", nextNode: "find_wizard" },
    { text: "Kahraman ara", nextNode: "find_hero" },
  ],
};

scenarios.living_dragon_hunt.story.stay_in_city = {
  title: "Şehirde Kalma",
  text: `Şehirde kalmaya karar veriyorsun. Güvenli bir yer.`,
  choices: [
    { text: "Yeni hayat", nextNode: "new_life" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.stay_in_forest = {
  title: "Ormanda Kalma",
  text: `Ormanda kalmaya karar veriyorsun. Doğayla iç içe.`,
  choices: [
    { text: "Yeni hayat", nextNode: "new_life" },
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.new_life = {
  title: "Yeni Hayat",
  text: `Yeni bir hayata başlıyorsun. Maceran burada biter.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
    { text: "Baştan başla", nextNode: "start_over" },
  ],
};

scenarios.living_dragon_hunt.story.attack_dragon = {
  title: "Ejderhaya Saldırma",
  text: `Ejderhaya saldırıyorsun. Kılıcınla savaşıyorsun.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight" },
    { text: "Geri çekil", nextNode: "retreat_from_battle" },
    { text: "Barış teklif et", nextNode: "offer_peace" },
  ],
};

scenarios.living_dragon_hunt.story.retreat_from_cave = {
  title: "Mağaradan Geri Çekilme",
  text: `Mağaradan geri çekiliyorsun. Ejderha çok güçlü.`,
  choices: [
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Plan yap", nextNode: "make_plan" },
    { text: "Yardım iste", nextNode: "ask_for_help" },
  ],
};

scenarios.living_dragon_hunt.story.convince_villagers = {
  title: "Köylüleri İkna Etme",
  text: `Köylüleri ejderha ile barış yapmaya ikna ediyorsun.`,
  choices: [
    { text: "Barış anlaşması yap", nextNode: "make_peace_deal" },
    { text: "Ejderhayı koru", nextNode: "protect_dragon" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.stay_in_village = {
  title: "Köyde Kalma",
  text: `Köyde kalmaya karar veriyorsun. Bu senin evin.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Koruyucu ol", nextNode: "become_protector" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.retreat_from_battle = {
  title: "Savaştan Geri Çekilme",
  text: `Savaştan geri çekiliyorsun. Ejderha çok güçlü.`,
  choices: [
    { text: "Geri dön", nextNode: "return_to_village" },
    { text: "Plan yap", nextNode: "make_plan" },
    { text: "Yardım iste", nextNode: "ask_for_help" },
  ],
};

scenarios.living_dragon_hunt.story.join_battle = {
  title: "Savaşa Katılma",
  text: `Savaşa katılıyorsun. Askerlerle birlikte ejderhaya karşı.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight" },
    { text: "Geri çekil", nextNode: "retreat_from_battle" },
    { text: "Zafer kazan", nextNode: "victory" },
  ],
};

scenarios.living_dragon_hunt.story.watch_battle = {
  title: "Savaşı İzleme",
  text: `Savaşı izliyorsun. Askerler ejderhaya karşı savaşıyor.`,
  choices: [
    { text: "Katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "spy_on_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.fight_with_wizard = {
  title: "Büyücüyle Savaşma",
  text: `Büyücüyle birlikte ejderhaya karşı savaşıyorsun.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight" },
    { text: "Geri çekil", nextNode: "retreat_from_battle" },
    { text: "Zafer kazan", nextNode: "victory" },
  ],
};

scenarios.living_dragon_hunt.story.fight_with_hero = {
  title: "Kahramanla Savaşma",
  text: `Kahramanla birlikte ejderhaya karşı savaşıyorsun.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight" },
    { text: "Geri çekil", nextNode: "retreat_from_battle" },
    { text: "Zafer kazan", nextNode: "victory" },
  ],
};

scenarios.living_dragon_hunt.story.continue_fight = {
  title: "Savaşa Devam Etme",
  text: `Savaşa devam ediyorsun. Ejderha güçlü ama sen de güçlüsün.`,
  choices: [
    { text: "Zafer kazan", nextNode: "victory" },
    { text: "Geri çekil", nextNode: "retreat_from_battle" },
    { text: "Barış teklif et", nextNode: "offer_peace" },
  ],
};

scenarios.living_dragon_hunt.story.victory = {
  title: "Zafer",
  text: `Ejderhaya karşı zafer kazandın! Köy artık güvende.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.spy_on_battle = {
  title: "Savaşı Gözetleme",
  text: `Savaşı gizlice gözetliyorsun. Askerler ejderhaya karşı savaşıyor.`,
  choices: [
    { text: "Katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

// WARHAMMER EKSİK NODE'LAR - SON
scenarios.warhammer_imperial_crisis.story.call_space_marines = {
  title: "Space Marine Çağırma",
  text: `Space Marine'ları çağırıyorsun. Chaos'a karşı güçlü müttefikler.`,
  choices: [
    { text: "Savaşa katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.call_imperial_guard = {
  title: "İmperial Guard Çağırma",
  text: `İmperial Guard'ı çağırıyorsun. Chaos'a karşı güçlü ordu.`,
  choices: [
    { text: "Savaşa katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.attack_cult = {
  title: "Külte Saldırma",
  text: `Chaos kültüne saldırıyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight_warhammer" },
    { text: "Geri çekil", nextNode: "retreat_from_temple" },
    { text: "Zafer kazan", nextNode: "victory_warhammer" },
  ],
};

scenarios.warhammer_imperial_crisis.story.set_trap_warhammer = {
  title: "Tuzak Kurma",
  text: `Chaos kültü için tuzak kuruyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Saldır", nextNode: "attack_cult" },
    { text: "Bekle", nextNode: "wait_for_cult" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.wait_for_help = {
  title: "Yardım Bekleme",
  text: `İmperium'dan yardım bekliyorsun. Space Marine'lar geliyor.`,
  choices: [
    { text: "Savaşa katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "watch_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.accept_mission = {
  title: "Görevi Kabul Etme",
  text: `Yeni İmperial görevi kabul ediyorsun. Chaos'a karşı savaşmaya devam edeceksin.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.reject_mission = {
  title: "Görevi Reddetme",
  text: `İmperial görevi reddediyorsun. Dinlenme zamanı.`,
  choices: [
    { text: "Dinlen", nextNode: "rest_peacefully" },
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.continue_fight_warhammer = {
  title: "Savaşa Devam Etme",
  text: `Chaos'a karşı savaşa devam ediyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Zafer kazan", nextNode: "victory_warhammer" },
    { text: "Geri çekil", nextNode: "retreat_from_temple" },
    { text: "Yardım çağır", nextNode: "call_for_help" },
  ],
};

scenarios.warhammer_imperial_crisis.story.victory_warhammer = {
  title: "Warhammer Zaferi",
  text: `Chaos'a karşı zafer kazandın! İmperium güvende.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero_warhammer" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.warhammer_imperial_crisis.story.wait_for_cult = {
  title: "Kültü Bekleme",
  text: `Chaos kültünü bekliyorsun. Tuzak hazır.`,
  choices: [
    { text: "Saldır", nextNode: "attack_cult" },
    { text: "Gözetle", nextNode: "spy_on_cult" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.warhammer_imperial_crisis.story.destroy_chaos = {
  title: "Chaos'u Yok Etme",
  text: `Chaos'u yok ediyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Zafer kazan", nextNode: "victory_warhammer" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

// EKSİK NODE'LAR - SON
scenarios.living_dragon_hunt.story.more_weapons = {
  title: "Daha Fazla Silah",
  text: `Daha fazla silah hazırlıyorsun. Köylülerle birlikte.`,
  choices: [
    { text: "Savaşa hazırlan", nextNode: "prepare_for_battle" },
    { text: "Ejderhayı bekle", nextNode: "wait_for_dragon" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.fight_cult = {
  title: "Kültle Savaşma",
  text: `Chaos kültüyle savaşıyorsun. Kutsal kolyenin gücüyle.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight_warhammer" },
    { text: "Geri çekil", nextNode: "retreat_from_temple" },
    { text: "Zafer kazan", nextNode: "victory_warhammer" },
  ],
};

scenarios.living_dragon_hunt.story.join_battle = {
  title: "Savaşa Katılma",
  text: `Savaşa katılıyorsun. Space Marine'larla birlikte.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight_warhammer" },
    { text: "Geri çekil", nextNode: "retreat_from_temple" },
    { text: "Zafer kazan", nextNode: "victory_warhammer" },
  ],
};

scenarios.living_dragon_hunt.story.watch_battle = {
  title: "Savaşı İzleme",
  text: `Savaşı izliyorsun. Space Marine'lar Chaos'a karşı savaşıyor.`,
  choices: [
    { text: "Katıl", nextNode: "join_battle" },
    { text: "Gözetle", nextNode: "spy_on_battle" },
    { text: "Geri dön", nextNode: "return_to_village" },
  ],
};

scenarios.living_dragon_hunt.story.return_to_village = {
  title: "Köye Dönüş",
  text: `Köye dönüyorsun. Hikayen burada biter.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
    { text: "Baştan başla", nextNode: "start_over" },
  ],
};

// EKSİK NODE'LAR - DEVAMI
// FANTASY EKSİK NODE'LAR
scenarios.living_dragon_hunt.story.talk_to_dragon = {
  title: "Ejderha ile Konuşma",
  text: `Ejderha ile konuşuyorsun. "Neden köyü yakıyorsun?" diye soruyorsun.
  
  "Köylüler beni rahatsız ediyor," diyor ejderha. "Ama sen farklısın."
  
  Ejderha seni dinliyor ve anlamaya çalışıyor.`,
  choices: [
    { text: "Barış teklif et", nextNode: "offer_peace" },
    { text: "Köylüleri savun", nextNode: "defend_villagers" },
    { text: "Anlaşma yap", nextNode: "make_deal" },
  ],
};

scenarios.living_dragon_hunt.story.defend_villagers = {
  title: "Köylüleri Savunma",
  text: `Köylüleri savunuyorsun. "Köylüler masum!" diye bağırıyorsun.
  
  "Onlar sadece yaşamaya çalışıyor," diyorsun. "Seni rahatsız etmek istemiyorlar."
  
  Ejderha düşünüyor ve senin haklı olduğunu anlıyor.`,
  choices: [
    { text: "Barış sağla", nextNode: "make_peace_deal" },
    { text: "Köylüleri koru", nextNode: "protect_villagers" },
    { text: "Yeni anlaşma", nextNode: "new_agreement" },
  ],
};

scenarios.living_dragon_hunt.story.make_deal = {
  title: "Anlaşma Yapma",
  text: `Ejderha ile anlaşma yapıyorsun. Köylüler ejderhaya saygı gösterecek, ejderha da köyü yakmayacak.
  
  "Bu anlaşma herkes için iyi," diyorsun.
  
  Hem köylüler hem ejderha mutlu.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

scenarios.living_dragon_hunt.story.protect_villagers = {
  title: "Köylüleri Koruma",
  text: `Köylüleri koruyorsun. Ejderhaya karşı onları savunuyorsun.
  
  "Köylüleri koruyacağım!" diye bağırıyorsun.
  
  Köylüler sana güveniyor ve seni kahraman olarak görüyorlar.`,
  choices: [
    { text: "Koruyucu ol", nextNode: "become_protector" },
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
  ],
};

scenarios.living_dragon_hunt.story.new_agreement = {
  title: "Yeni Anlaşma",
  text: `Ejderha ile yeni bir anlaşma yapıyorsun. Bu sefer daha detaylı ve adil.
  
  "Herkes kazanacak," diyorsun.
  
  Anlaşma başarılı ve herkes mutlu.`,
  choices: [
    { text: "Kahraman ol", nextNode: "become_hero" },
    { text: "Köyde kal", nextNode: "stay_in_village" },
    { text: "Yeni macera", nextNode: "new_adventure" },
  ],
};

// WARHAMMER EKSİK NODE'LAR
scenarios.warhammer_imperial_crisis.story.fight_dragon = {
  title: "Ejderha ile Savaşma",
  text: `Ejderha ile savaşıyorsun. Kılıcınla güçlü darbeler indiriyorsun.
  
  "Köyü koruyacağım!" diye bağırıyorsun.
  
  Savaş zorlu ama sen kararlısın.`,
  choices: [
    { text: "Savaşa devam et", nextNode: "continue_fight" },
    { text: "Güç kullan", nextNode: "use_power" },
    { text: "Yardım çağır", nextNode: "call_help" },
  ],
};

scenarios.warhammer_imperial_crisis.story.use_power = {
  title: "Güç Kullanma",
  text: `Özel gücünü kullanıyorsun. Büyü veya özel yeteneklerinle ejderhaya saldırıyorsun.
  
  "Gücümü kullanacağım!" diye bağırıyorsun.
  
  Ejderha şaşkın ve gücünü görünce korkuyor.`,
  choices: [
    { text: "Zafer kazan", nextNode: "victory" },
    { text: "Savaşa devam et", nextNode: "continue_fight" },
    { text: "Barış teklif et", nextNode: "offer_peace" },
  ],
};

scenarios.warhammer_imperial_crisis.story.call_help = {
  title: "Yardım Çağırma",
  text: `Yardım çağırıyorsun. Köylüler ve diğer kahramanlar sana yardım ediyor.
  
  "Yardım edin!" diye bağırıyorsun.
  
  Birlikte ejderhaya karşı savaşıyorsunuz.`,
  choices: [
    { text: "Birlikte savaş", nextNode: "join_battle" },
    { text: "Zafer kazan", nextNode: "victory" },
    { text: "Gözetle", nextNode: "watch_battle" },
  ],
};

// CYBERPUNK EKSİK NODE'LAR
scenarios.cyberpunk_hive_city.story.happy_ending = {
  title: "Cyberpunk Mutlu Son",
  text: `Hive City'de mutlu bir hayat yaşıyorsun. Şirketlere karşı savaşan en iyi netrunner'lardan birisin.
  
  "Bu benim dünyam," diyorsun. "Ve değiştireceğim."
  
  Hive City'de yeni bir düzen kuruyorsun.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
    { text: "Baştan başla", nextNode: "start_over" },
  ],
};

scenarios.cyberpunk_hive_city.story.new_life = {
  title: "Yeni Hayat",
  text: `Hive City'den ayrılıyorsun. Yeni bir hayata başlıyorsun.
  
  "Burada yapacak işim kalmadı," diyorsun.
  
  Yeni maceralar seni bekliyor.`,
  choices: [
    { text: "Yeni macera", nextNode: "new_adventure" },
    { text: "Dinlen", nextNode: "rest_peacefully" },
    { text: "Baştan başla", nextNode: "start_over" },
  ],
};

// MISSING NODES - COMPLETE STORY BRANCHES
console.log("=== MISSING NODES LOADED ===");

// Add missing nodes to existing scenarios
if (window.scenarios && window.scenarios.living_dragon_hunt) {
  // Add missing nodes to living_dragon_hunt scenario
  window.scenarios.living_dragon_hunt.story = {
    ...window.scenarios.living_dragon_hunt.story,

    // Mission acceptance nodes
    accept_mission: {
      title: "Görevi Kabul Et",
      text: `Görevi kabul ettin! Artık ejderhayı durdurmak için resmi olarak görevlendirildin. Köy meclisi sana güveniyor ve tüm kaynakları kullanmana izin veriyor.`,
      choices: [
        { text: "Hemen yola çık", nextNode: "start_journey" },
        { text: "Önce hazırlık yap", nextNode: "prepare_for_journey" },
        { text: "Bilgi topla", nextNode: "gather_information" },
        { text: "Müttefik ara", nextNode: "seek_allies" },
      ],
    },

    start_journey: {
      title: "Yolculuk Başlıyor",
      text: `Ejderhayı aramak için yola çıktın. Dağların eteklerinde ilerliyorsun ve her adımda tehlike artıyor.`,
      choices: [
        { text: "Dağ yolunu takip et", nextNode: "mountain_path" },
        { text: "Mağaraları ara", nextNode: "search_caves" },
        { text: "Yerel rehber bul", nextNode: "find_local_guide" },
      ],
    },

    prepare_for_journey: {
      title: "Yolculuk Hazırlığı",
      text: `Yolculuk için hazırlık yapıyorsun. Silahlarını keskinleştiriyor, zırhını kontrol ediyorsun.`,
      choices: [
        { text: "Silahları hazırla", nextNode: "prepare_weapons" },
        { text: "İksirler al", nextNode: "get_potions" },
        { text: "Harita al", nextNode: "get_map" },
      ],
    },

    gather_information: {
      title: "Bilgi Toplama",
      text: `Ejderha hakkında daha fazla bilgi toplamaya karar verdin. Köylülerle konuşuyorsun.`,
      choices: [
        { text: "Görgü tanıklarıyla konuş", nextNode: "talk_witnesses" },
        { text: "Eski kayıtları ara", nextNode: "search_records" },
        { text: "Büyücüye danış", nextNode: "consult_wizard" },
      ],
    },

    seek_allies: {
      title: "Müttefik Arama",
      text: `Bu görev için müttefikler bulmaya karar verdin. Tek başına ejderhayla savaşmak çok tehlikeli.`,
      choices: [
        { text: "Yakındaki şehre git", nextNode: "go_to_nearby_city" },
        { text: "Kahraman ara", nextNode: "find_hero" },
        { text: "Büyücü topluluğuna git", nextNode: "wizard_guild" },
      ],
    },

    mountain_path: {
      title: "Dağ Yolu",
      text: `Dağ yolunu takip ediyorsun. Yüksek irtifada nefes almak zorlaşıyor ve hava soğuk.`,
      choices: [
        { text: "Devam et", nextNode: "continue_mountain_path" },
        { text: "Dinlen", nextNode: "rest_on_mountain" },
        { text: "Alternatif yol ara", nextNode: "find_alternative_path" },
      ],
    },

    search_caves: {
      title: "Mağara Arama",
      text: `Mağaraları aramaya başladın. Karanlık ve nemli mağaralarda ejderhanın izlerini arıyorsun.`,
      choices: [
        { text: "Derinlere in", nextNode: "go_deeper_caves" },
        { text: "Mağara sistemini haritalandır", nextNode: "map_cave_system" },
        { text: "Çıkış ara", nextNode: "find_cave_exit" },
      ],
    },

    find_local_guide: {
      title: "Yerel Rehber Bulma",
      text: `Yerel bir rehber bulmaya karar verdin. Bu bölgeyi iyi bilen biri sana yardım edebilir.`,
      choices: [
        { text: "Avcılarla konuş", nextNode: "talk_hunters" },
        { text: "Çobanlarla konuş", nextNode: "talk_shepherds" },
        { text: "Tüccarlarla konuş", nextNode: "talk_merchants" },
      ],
    },

    continue_mountain_path: {
      title: "Dağ Yoluna Devam",
      text: `Dağ yoluna devam ediyorsun. Uzaktan ejderhanın alevlerini görebiliyorsun.`,
      choices: [
        { text: "Alevlerin kaynağına git", nextNode: "go_to_flame_source" },
        { text: "Gözetle", nextNode: "spy_on_dragon" },
        { text: "Plan yap", nextNode: "plan_attack" },
      ],
    },

    go_to_flame_source: {
      title: "Alevlerin Kaynağı",
      text: `Alevlerin kaynağına ulaştın. Büyük bir mağara girişi var ve içeriden sıcak hava geliyor.`,
      choices: [
        { text: "Mağaraya gir", nextNode: "enter_dragon_cave" },
        { text: "Önce gözetle", nextNode: "scout_cave_entrance" },
        { text: "Tuzak kur", nextNode: "set_trap" },
      ],
    },

    enter_dragon_cave: {
      title: "Ejderha Mağarası",
      text: `Mağaraya girdin. İçeride büyük bir ejderha yatıyor ve seni fark etti!`,
      choices: [
        { text: "Savaş", nextNode: "dragon_battle" },
        { text: "Konuşmaya çalış", nextNode: "try_to_negotiate" },
        { text: "Kaç", nextNode: "flee_from_dragon" },
      ],
    },

    dragon_battle: {
      title: "Ejderha Savaşı",
      text: `Ejderhayla savaşa girdin! Bu çok tehlikeli bir düşman.`,
      choices: [
        { text: "Güçlü saldırı", nextNode: "strong_attack" },
        { text: "Savunma yap", nextNode: "defend_against_dragon" },
        { text: "Büyü kullan", nextNode: "use_magic" },
      ],
    },

    strong_attack: {
      title: "Güçlü Saldırı",
      text: `Ejderhaya güçlü bir saldırı yaptın! Ama o da sana saldırıyor.`,
      choices: [
        { text: "Devam et", nextNode: "continue_battle" },
        { text: "Strateji değiştir", nextNode: "change_strategy" },
        { text: "Yardım ara", nextNode: "call_for_help" },
      ],
    },

    continue_battle: {
      title: "Savaşa Devam",
      text: `Savaşa devam ediyorsun. Ejderha yaralandı ama hala çok güçlü.`,
      choices: [
        { text: "Son saldırı", nextNode: "final_attack" },
        { text: "Zayıf noktasını ara", nextNode: "find_weakness" },
        { text: "Barış teklifi yap", nextNode: "offer_peace" },
      ],
    },

    final_attack: {
      title: "Son Saldırı",
      text: `Son saldırını yaptın! Ejderha yere düştü ve artık hareket etmiyor.`,
      choices: [
        { text: "Ejderhayı öldür", nextNode: "kill_dragon" },
        { text: "Ejderhayı affet", nextNode: "spare_dragon" },
        { text: "Ejderhayı yakala", nextNode: "capture_dragon" },
      ],
    },

    kill_dragon: {
      title: "Ejderhayı Öldür",
      text: `Ejderhayı öldürdün. Köy artık güvende ama senin içinde bir boşluk var.`,
      choices: [
        { text: "Köye dön", nextNode: "return_to_village_victory" },
        {
          text: "Ejderhanın hazinesini ara",
          nextNode: "search_dragon_treasure",
        },
        { text: "Yeni macera ara", nextNode: "seek_new_adventure" },
      ],
    },

    return_to_village_victory: {
      title: "Zaferle Dönüş",
      text: `Köye zaferle döndün! Köylüler seni kahraman olarak karşılıyor.`,
      choices: [
        { text: "Kutlamaya katıl", nextNode: "celebrate_victory" },
        { text: "Yeni görev ara", nextNode: "seek_new_mission" },
        { text: "Dinlen", nextNode: "rest_and_recover" },
      ],
    },

    celebrate_victory: {
      title: "Zafer Kutlaması",
      text: `Köyde büyük bir kutlama var. Sen artık efsanevi bir kahramansın!`,
      choices: [
        { text: "Hikayeni anlat", nextNode: "tell_story" },
        { text: "Yeni macera ara", nextNode: "seek_new_adventure" },
        { text: "Köyde kal", nextNode: "stay_in_village" },
      ],
    },

    // Additional nodes for complete story
    prepare_weapons: {
      title: "Silah Hazırlığı",
      text: `Silahlarını hazırlıyorsun. Kılıcını keskinleştiriyor, oklarını kontrol ediyorsun.`,
      choices: [
        { text: "Yola çık", nextNode: "start_journey" },
        { text: "Daha fazla hazırlık", nextNode: "more_preparation" },
      ],
    },

    get_potions: {
      title: "İksir Alma",
      text: `Köyün şifacısından iksirler aldın. Can iksiri, güç iksiri ve zehir panzehiri.`,
      choices: [
        { text: "Yola çık", nextNode: "start_journey" },
        { text: "Daha fazla iksir al", nextNode: "get_more_potions" },
      ],
    },

    get_map: {
      title: "Harita Alma",
      text: `Köyün haritacısından detaylı bir harita aldın. Dağlar, mağaralar ve gizli yollar işaretli.`,
      choices: [
        { text: "Yola çık", nextNode: "start_journey" },
        { text: "Haritayı incele", nextNode: "study_map" },
      ],
    },

    talk_witnesses: {
      title: "Görgü Tanıkları",
      text: `Ejderhayı gören köylülerle konuştun. Büyük, kırmızı bir ejderha olduğunu öğrendin.`,
      choices: [
        { text: "Yola çık", nextNode: "start_journey" },
        { text: "Daha fazla bilgi ara", nextNode: "search_more_info" },
      ],
    },

    search_records: {
      title: "Eski Kayıtlar",
      text: `Köyün kütüphanesinde eski kayıtları inceledin. Bu ejderhanın daha önce de saldırdığını öğrendin.`,
      choices: [
        { text: "Yola çık", nextNode: "start_journey" },
        { text: "Daha fazla araştır", nextNode: "research_more" },
      ],
    },

    consult_wizard: {
      title: "Büyücüye Danışma",
      text: `Köyün büyücüsüyle konuştun. Ejderhanın zayıf noktalarını ve nasıl yenileceğini öğrendin.`,
      choices: [
        { text: "Yola çık", nextNode: "start_journey" },
        { text: "Büyü öğren", nextNode: "learn_magic" },
      ],
    },

    go_to_nearby_city: {
      title: "Yakındaki Şehir",
      text: `Yakındaki şehre gittin. Burada profesyonel ejderha avcıları var.`,
      choices: [
        { text: "Avcılarla konuş", nextNode: "talk_professional_hunters" },
        { text: "Şehirde kal", nextNode: "stay_in_city" },
      ],
    },

    find_hero: {
      title: "Kahraman Bulma",
      text: `Bölgede ünlü bir kahraman olduğunu duydun. Onu bulmaya karar verdin.`,
      choices: [
        { text: "Kahramanı ara", nextNode: "search_for_hero" },
        { text: "Başka yöntem dene", nextNode: "try_other_method" },
      ],
    },

    wizard_guild: {
      title: "Büyücü Topluluğu",
      text: `Büyücü topluluğuna gittin. Burada güçlü büyücüler var.`,
      choices: [
        { text: "Büyücülerle konuş", nextNode: "talk_wizards" },
        { text: "Büyü öğren", nextNode: "learn_from_wizards" },
      ],
    },

    // Battle and combat nodes
    defend_against_dragon: {
      title: "Ejderhaya Karşı Savunma",
      text: `Ejderhanın saldırısına karşı savunma yapıyorsun. Kalkanını kullanıyorsun.`,
      choices: [
        { text: "Karşı saldırı", nextNode: "counter_attack" },
        { text: "Kaç", nextNode: "flee_from_battle" },
      ],
    },

    use_magic: {
      title: "Büyü Kullanma",
      text: `Ejderhaya karşı büyü kullanıyorsun. Ateş topu fırlatıyorsun!`,
      choices: [
        { text: "Büyüye devam et", nextNode: "continue_magic" },
        { text: "Fiziksel saldırı", nextNode: "physical_attack" },
      ],
    },

    try_to_negotiate: {
      title: "Müzakere Denemesi",
      text: `Ejderhayla konuşmaya çalışıyorsun. Belki barışçıl bir çözüm bulabilirsin.`,
      choices: [
        { text: "Anlaşma yap", nextNode: "make_deal" },
        { text: "Savaşa devam et", nextNode: "continue_fighting" },
      ],
    },

    flee_from_dragon: {
      title: "Ejderhadan Kaçma",
      text: `Ejderhadan kaçıyorsun. Bu çok tehlikeli bir durum!`,
      choices: [
        { text: "Güvenli yere kaç", nextNode: "escape_to_safety" },
        { text: "Geri dön", nextNode: "return_to_village" },
      ],
    },

    // Victory and ending nodes
    spare_dragon: {
      title: "Ejderhayı Affetme",
      text: `Ejderhayı öldürmek yerine affettin. O da sana minnettar.`,
      choices: [
        { text: "Köye dön", nextNode: "return_to_village_peace" },
        { text: "Ejderhayla arkadaş ol", nextNode: "befriend_dragon" },
      ],
    },

    capture_dragon: {
      title: "Ejderhayı Yakalama",
      text: `Ejderhayı yakaladın. Artık onu kontrol edebilirsin.`,
      choices: [
        { text: "Köye götür", nextNode: "bring_dragon_to_village" },
        { text: "Serbest bırak", nextNode: "release_dragon" },
      ],
    },

    search_dragon_treasure: {
      title: "Ejderha Hazinesi",
      text: `Ejderhanın mağarasında büyük bir hazine buldun! Altın, mücevherler ve büyülü eşyalar var.`,
      choices: [
        { text: "Hepsini al", nextNode: "take_all_treasure" },
        { text: "Köyle paylaş", nextNode: "share_with_village" },
      ],
    },

    seek_new_adventure: {
      title: "Yeni Macera Arama",
      text: `Yeni maceralar arıyorsun. Dünya büyük ve keşfedilecek çok şey var.`,
      choices: [
        { text: "Uzak diyarlara git", nextNode: "go_to_distant_lands" },
        { text: "Yeni görev ara", nextNode: "find_new_quest" },
      ],
    },

    tell_story: {
      title: "Hikaye Anlatma",
      text: `Köylülere maceranı anlatıyorsun. Herkes seni dinliyor ve hayran kalıyor.`,
      choices: [
        { text: "Devam et", nextNode: "continue_storytelling" },
        { text: "Yeni macera ara", nextNode: "seek_new_adventure" },
      ],
    },

    stay_in_village: {
      title: "Köyde Kalma",
      text: `Köyde kalmaya karar verdin. Artık bu senin evin.`,
      choices: [
        { text: "Köyü koru", nextNode: "protect_village" },
        { text: "Yeni macera ara", nextNode: "seek_new_adventure" },
      ],
    },

    // Fallback nodes for any missing choices
    default_node: {
      title: "Macera Devam Ediyor",
      text: `Macera devam ediyor! Yeni fırsatlar seni bekliyor.`,
      choices: [
        { text: "Devam et", nextNode: "continue_adventure" },
        { text: "Yeni yol ara", nextNode: "find_new_path" },
      ],
    },

    continue_adventure: {
      title: "Macereye Devam",
      text: `Macereye devam ediyorsun. Her adımda yeni bir keşif yapıyorsun.`,
      choices: [
        { text: "Keşfet", nextNode: "explore_more" },
        { text: "Dinlen", nextNode: "rest_and_continue" },
      ],
    },

    find_new_path: {
      title: "Yeni Yol Bulma",
      text: `Yeni bir yol buldun. Bu yol seni nereye götürecek?`,
      choices: [
        { text: "Bu yolu takip et", nextNode: "follow_new_path" },
        { text: "Geri dön", nextNode: "go_back" },
      ],
    },
  };
}

// Add missing nodes to Warhammer scenario
if (window.scenarios && window.scenarios.warhammer_imperial_crisis) {
  window.scenarios.warhammer_imperial_crisis.story = {
    ...window.scenarios.warhammer_imperial_crisis.story,

    recover_memory_warhammer: {
      title: "Hafıza Geri Getirme",
      text: `Hafızanı geri getirmeye çalışıyorsun. Boynundaki kolye parlamaya başladı.`,
      choices: [
        { text: "Kolyeyi kullan", nextNode: "use_necklace" },
        { text: "Meditasyon yap", nextNode: "meditate" },
      ],
    },

    examine_necklace_warhammer: {
      title: "Kolyeyi İnceleme",
      text: `Kolyeyi inceliyorsun. Üzerinde İmperium'un sembolü var.`,
      choices: [
        { text: "Kolyeyi tak", nextNode: "wear_necklace" },
        { text: "Daha fazla incele", nextNode: "examine_more" },
      ],
    },

    explore_village: {
      title: "Köyü Keşfetme",
      text: `Köyü keşfediyorsun. İmperium'un bir dünyasında olduğunu anlıyorsun.`,
      choices: [
        { text: "Köylülerle konuş", nextNode: "talk_villagers" },
        { text: "Köyü araştır", nextNode: "investigate_village" },
      ],
    },

    seek_help_warhammer: {
      title: "Yardım Arama",
      text: `Yardım aramaya karar verdin. Bu dünyada İmperium'un güçleri var.`,
      choices: [
        { text: "İmperial Guard ara", nextNode: "find_imperial_guard" },
        { text: "Inquisitor ara", nextNode: "find_inquisitor" },
      ],
    },
  };
}

// Add missing nodes to Cyberpunk scenario
if (window.scenarios && window.scenarios.cyberpunk_hive_city) {
  window.scenarios.cyberpunk_hive_city.story = {
    ...window.scenarios.cyberpunk_hive_city.story,

    hack_system: {
      title: "Sistemi Hack Etme",
      text: `Neural implant'ını kullanarak sistemi hack etmeye çalışıyorsun.`,
      choices: [
        { text: "Hack'e devam et", nextNode: "continue_hacking" },
        { text: "Sistemi analiz et", nextNode: "analyze_system" },
      ],
    },

    go_upstairs: {
      title: "Yukarı Çıkma",
      text: `Hive City'nin üst katmanlarına çıkmaya çalışıyorsun.`,
      choices: [
        { text: "Asansör kullan", nextNode: "use_elevator" },
        { text: "Merdivenleri kullan", nextNode: "use_stairs" },
      ],
    },

    search_data: {
      title: "Veri Arama",
      text: `Çevredeki veri terminallerinde bilgi arıyorsun.`,
      choices: [
        { text: "Veri analiz et", nextNode: "analyze_data" },
        { text: "Veri çal", nextNode: "steal_data" },
      ],
    },

    escape_hive: {
      title: "Hive'dan Kaçma",
      text: `Hive City'den kaçmaya çalışıyorsun. Bu tehlikeli bir işlem.`,
      choices: [
        { text: "Gizli çıkış ara", nextNode: "find_secret_exit" },
        { text: "Güvenli yol ara", nextNode: "find_safe_route" },
      ],
    },
  };
}

console.log("✅ All missing nodes have been added to scenarios");
