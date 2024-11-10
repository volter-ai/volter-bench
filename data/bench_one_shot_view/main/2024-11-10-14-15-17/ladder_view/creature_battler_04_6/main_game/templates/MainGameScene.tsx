import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

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

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  // Filter skills based on available button slugs if they exist
  const availableSkills = playerCreature.collections.skills?.filter(skill => 
    !availableButtonSlugs?.length || availableButtonSlugs.includes(skill.uid)
  ) || []

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-100">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 grid grid-cols-2 p-4 gap-4">
        {/* Top row */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/creatures/${opponentCreature.uid}`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
        
        <div className="flex items-start justify-center">
          <div className="relative">
            <div className="w-48 h-48 flex items-center justify-center">
              {/* Opponent creature placeholder - front view */}
              <div className="w-32 h-32 bg-slate-300 rounded-full flex items-center justify-center">
                {opponentCreature.display_name[0]}
              </div>
            </div>
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom row */}
        <div className="flex items-end justify-center">
          <div className="relative">
            <div className="w-48 h-48 flex items-center justify-center">
              {/* Player creature placeholder - back view */}
              <div className="w-32 h-32 bg-slate-300 rounded-full flex items-center justify-center">
                {playerCreature.display_name[0]}
              </div>
            </div>
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/creatures/${playerCreature.uid}`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 bg-white p-4">
        {availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 h-full">
            {availableSkills.map((skill) => (
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
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">No actions available</p>
          </div>
        )}
      </div>
    </div>
  )
}
