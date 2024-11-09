import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
  meta: {
    prototype_id: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
  meta: {
    prototype_id: string
  }
}

interface GameUIData {
  entities: {
    player: Player
    foe: Player
    player_creature: Creature
    foe_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, foe, player_creature, foe_creature } = props.data.entities

  const handleSkillClick = (skillUid: string) => {
    if (!skillUid) return;
    
    // Format the button slug consistently
    const expectedSlug = `skill_${skillUid}`.toLowerCase();
    
    // Find the matching available button slug
    const buttonSlug = availableButtonSlugs.find(slug => 
      slug.toLowerCase() === expectedSlug
    );
    
    if (buttonSlug) {
      emitButtonClick(buttonSlug);
    }
  }

  return (
    <div className="w-full h-full aspect-video bg-background flex flex-col">
      {/* HUD */}
      <nav className="w-full p-4 bg-muted flex justify-between items-center">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta.prototype_id}.png`}
          />
        )}
        <div className="flex items-center gap-2">
          <Swords className="w-5 h-5" />
          <span>Battle Phase</span>
        </div>
        {foe && (
          <PlayerCard
            uid={foe.uid}
            name={foe.display_name}
            imageUrl={`/players/${foe.meta.prototype_id}.png`}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8 py-4">
        {player_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Your Creature
            </span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
            />
          </div>
        )}

        {foe_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Opponent's Creature
            </span>
            <CreatureCard
              uid={foe_creature.uid}
              name={foe_creature.display_name}
              hp={foe_creature.stats.hp}
              maxHp={foe_creature.stats.max_hp}
              imageUrl={`/creatures/${foe_creature.meta.prototype_id}.png`}
            />
          </div>
        )}
      </div>

      {/* Skills UI */}
      <div className="p-4 bg-muted">
        <div className="flex flex-wrap gap-2 justify-center">
          {player_creature?.collections.skills?.map((skill) => {
            const expectedSlug = `skill_${skill.uid}`.toLowerCase();
            const isAvailable = availableButtonSlugs.some(slug => 
              slug.toLowerCase() === expectedSlug
            );
            
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!isAvailable}
                onClick={() => handleSkillClick(skill.uid)}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}
