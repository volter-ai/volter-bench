import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
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
  }
  collections?: {
    skills?: Skill[]
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

interface GameUIData {
  uid: string
  entities: {
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div uid="loading-container" className="w-screen h-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div uid={props.data.uid} className="w-screen h-screen flex flex-col bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div uid={`${props.data.uid}-battlefield`} className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div uid={`${props.data.uid}-opponent-status`} className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.creature_type}_front.png`}
          />
        </div>

        {/* Opponent Creature */}
        <div uid={`${props.data.uid}-opponent-creature`} className="flex items-center justify-center">
          <div uid={`${opponentCreature.uid}-sprite-container`} className="relative">
            <div 
              uid={`${opponentCreature.uid}-shadow`} 
              className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" 
            />
            <img
              uid={`${opponentCreature.uid}-sprite`}
              src={`/creatures/${opponentCreature.meta.creature_type}_front.png`}
              alt={opponentCreature.display_name}
              className="w-32 h-32 object-contain"
            />
          </div>
        </div>

        {/* Player Creature */}
        <div uid={`${props.data.uid}-player-creature`} className="flex items-center justify-center">
          <div uid={`${playerCreature.uid}-sprite-container`} className="relative">
            <div 
              uid={`${playerCreature.uid}-shadow`} 
              className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" 
            />
            <img
              uid={`${playerCreature.uid}-sprite`}
              src={`/creatures/${playerCreature.meta.creature_type}_back.png`}
              alt={playerCreature.display_name}
              className="w-32 h-32 object-contain"
            />
          </div>
        </div>

        {/* Player Status */}
        <div uid={`${props.data.uid}-player-status`} className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.creature_type}_back.png`}
          />
        </div>
      </div>

      {/* UI Area */}
      <div uid={`${props.data.uid}-ui-area`} className="h-1/3 bg-white/90 p-4">
        <div uid={`${props.data.uid}-skills-grid`} className="grid grid-cols-2 gap-4 h-full">
          {playerCreature.collections?.skills?.map((skill: Skill) => (
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
