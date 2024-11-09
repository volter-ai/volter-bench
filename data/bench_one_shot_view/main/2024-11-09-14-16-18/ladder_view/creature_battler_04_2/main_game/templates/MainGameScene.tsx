import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card" 
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  meta: {
    creature_type: string
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    skill_type: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  description: string
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature } = props.data.entities

  // Helper to get creature image URL based on prototype_id
  const getCreatureImageUrl = (prototypeId: string, isBack: boolean = false) => {
    return `/images/creatures/${prototypeId}${isBack ? '_back' : ''}.png`
  }

  return (
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl={getCreatureImageUrl(opponent_creature.meta.prototype_id)}
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {opponent_creature && (
            <div className="relative">
              <img 
                src={getCreatureImageUrl(opponent_creature.meta.prototype_id)}
                alt={opponent_creature.display_name}
                className="w-48 h-48 object-contain"
              />
              <div className="absolute bottom-0 w-full h-4 bg-black/20 blur-md" />
            </div>
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {player_creature && (
            <div className="relative">
              <img 
                src={getCreatureImageUrl(player_creature.meta.prototype_id, true)}
                alt={player_creature.display_name}
                className="w-48 h-48 object-contain"
              />
              <div className="absolute bottom-0 w-full h-4 bg-black/20 blur-md" />
            </div>
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={getCreatureImageUrl(player_creature.meta.prototype_id, true)}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 bg-white/90 rounded-t-xl shadow-lg">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
