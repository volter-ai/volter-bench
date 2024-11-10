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
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface GameUIData {
  entities: {
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs = [],
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const opponentCreature = props.data?.entities?.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-screen h-screen flex items-center justify-center">
      Loading...
    </div>
  }

  const availableSkills = playerCreature.collections.skills?.filter(skill => 
    availableButtonSlugs.includes(`skill_${skill.uid}`)
  ) || []

  const handleSkillClick = (skillUid: string) => {
    const buttonSlug = `skill_${skillUid}`
    if (availableButtonSlugs.includes(buttonSlug)) {
      emitButtonClick(buttonSlug)
    }
  }

  return (
    <div className="w-screen h-screen flex flex-col bg-gradient-to-b from-sky-100 to-sky-300">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow-[2] grid grid-cols-2 relative p-4 gap-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id || 'default'}_front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-end justify-end">
          <div className="relative">
            <img
              src={`/creatures/${opponentCreature.meta.prototype_id || 'default'}_front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-end justify-start">
          <div className="relative">
            <img
              src={`/creatures/${playerCreature.meta.prototype_id || 'default'}_back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id || 'default'}_front.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="flex-grow-[1] min-h-[200px] p-4 bg-white/80 relative z-10">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableSkills.length > 0 ? (
            availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                type={skill.meta.skill_type}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center text-gray-500">
              No actions available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
