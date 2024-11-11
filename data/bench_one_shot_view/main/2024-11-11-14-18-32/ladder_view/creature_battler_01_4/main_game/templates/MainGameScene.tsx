import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
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
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
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

  return (
    <div className="w-full h-full aspect-ratio-[16/9] flex flex-col">
      {/* HUD */}
      <nav className="w-full p-4 bg-slate-800 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Sword className="w-5 h-5" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12 py-6">
        {/* Player Side */}
        <div className="flex flex-col items-center gap-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder-player.png"
            />
          )}
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>

        {/* Opponent Side */}
        <div className="flex flex-col items-center gap-4">
          {foe && (
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl="/placeholder-player.png"
            />
          )}
          {foe_creature && (
            <CreatureCard
              uid={foe_creature.uid}
              name={foe_creature.display_name}
              hp={foe_creature.stats.hp}
              maxHp={foe_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>
      </div>

      {/* Controls */}
      <div className="h-1/4 bg-slate-900 p-4 overflow-y-auto">
        <div className="flex flex-wrap gap-2">
          {player_creature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
