import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react'
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
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
}

interface GameUIData {
  entities: {
    player_creature?: Creature
    opponent_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const opponentCreature = props.data?.entities?.opponent_creature

  // Comprehensive null checks
  if (!props.data?.entities) {
    return <div className="text-center p-4">No game data available</div>
  }

  if (!playerCreature || !opponentCreature) {
    return <div className="text-center p-4">Waiting for creatures...</div>
  }

  const playerSkills = playerCreature.collections?.skills || []

  return (
    <div className="h-screen w-full aspect-video flex flex-col bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 p-4 relative">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start p-4">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              imageUrl={`/creatures/${opponentCreature.uid}/front.png`}
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start p-4">
          {opponentCreature && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <img
                src={`/creatures/${opponentCreature.uid}/front.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            </div>
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end p-4">
          {playerCreature && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <img
                src={`/creatures/${playerCreature.uid}/back.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            </div>
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end p-4">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.uid}/front.png`}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-white/90 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerSkills.length > 0 ? (
            playerSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                type={skill.meta.skill_type}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center text-gray-500">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
