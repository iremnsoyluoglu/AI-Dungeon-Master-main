#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.core.campaign_manager import CampaignManager

def show_all_campaigns():
    cm = CampaignManager()
    campaigns = cm.list_campaigns()
    
    print("🎮 TÜM OYNABİLİR SENARYOLAR")
    print("=" * 60)
    print()
    
    total_scenes = 0
    total_combat_scenes = 0
    total_npc_interactions = 0
    
    for campaign in campaigns:
        campaign_id = campaign["id"]
        campaign_data = cm.get_campaign(campaign_id)
        
        if not campaign_data:
            continue
            
        scenes = campaign_data.get("scenes", [])
        scene_count = len(scenes)
        total_scenes += scene_count
        
        # Combat scene sayısını hesapla
        combat_scenes = 0
        npc_interactions = 0
        
        for scene in scenes:
            choices = scene.get("choices", [])
            for choice in choices:
                if choice.get("combat"):
                    combat_scenes += 1
                if "ally:" in str(choice.get("effect", "")):
                    npc_interactions += 1
                if "relationship:" in str(choice.get("effect", "")):
                    npc_interactions += 1
        
        total_combat_scenes += combat_scenes
        total_npc_interactions += npc_interactions
        
        print(f"📖 {campaign['name']}")
        print(f"   🆔 ID: {campaign_id}")
        print(f"   🎭 Tür: {campaign['type']}")
        print(f"   📝 Açıklama: {campaign['description']}")
        print(f"   🎬 Toplam Sahne: {scene_count}")
        print(f"   ⚔️ Savaş Sahnesi: {combat_scenes}")
        print(f"   👥 NPC Etkileşimi: {npc_interactions}")
        
        # Sahne listesi
        print(f"   🎯 Sahne Listesi:")
        for i, scene in enumerate(scenes, 1):
            scene_title = scene.get("title", "Bilinmeyen Sahne")
            print(f"      {i:2d}. {scene_title}")
        
        print()
        print("-" * 60)
        print()
    
    print("📊 GENEL İSTATİSTİKLER")
    print("=" * 60)
    print(f"🎬 Toplam Sahne Sayısı: {total_scenes}")
    print(f"⚔️ Toplam Savaş Sahnesi: {total_combat_scenes}")
    print(f"👥 Toplam NPC Etkileşimi: {total_npc_interactions}")
    print(f"📖 Toplam Kampanya Sayısı: {len(campaigns)}")
    print()
    print("🎮 Oyun Erişim: http://localhost:5000")

if __name__ == "__main__":
    show_all_campaigns() 