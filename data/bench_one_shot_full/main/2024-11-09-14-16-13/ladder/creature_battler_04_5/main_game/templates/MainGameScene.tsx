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
  collections: {
    creatures: Creature[]
  }
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

  const playerCreature = props.data?.entities?.player_creature
  const opponentCreature = props.data?.entities?.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs?.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  const skills = playerCreature.collections?.skills || []
  const availableSkills = skills.filter(skill => 
    availableButtonSlugs?.includes(skill.uid)
  )

  return (
    <div className="relative w-full h-full flex flex-col">
      {/* Battlefield Area */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          <div className="relative">
            <div className="w-48 h-48 bg-gray-200 rounded-lg flex items-center justify-center">
              {opponentCreature.display_name}
            </div>
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <div className="relative">
            <div className="w-48 h-48 bg-gray-200 rounded-lg flex items-center justify-center">
              {playerCreature.display_name}
            </div>
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white/5">
        <div className="p-4 grid grid-cols-2 gap-2 h-full">
          {availableSkills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
