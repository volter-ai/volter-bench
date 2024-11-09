import { useCurrentButtons } from "@/lib/useChoices.ts";
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
    attack: number
    defense: number
  }
  meta: {
    creature_type: string
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

interface GameUIData {
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

  const playerCreature = props.data?.entities?.player_creature
  const opponentCreature = props.data?.entities?.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="relative w-full h-full flex flex-col">
      {/* Battle Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-sky-100 to-sky-300" />

      {/* Battlefield Area */}
      <div className="relative flex-grow grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.creature_type}_front.png`}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          <CreatureCard
            uid={`${opponentCreature.uid}-battle`}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.creature_type}_front.png`}
            className="transform scale-150"
          />
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <CreatureCard
            uid={`${playerCreature.uid}-battle`}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.creature_type}_back.png`}
            className="transform scale-150"
          />
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
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
      <div className="relative h-1/3 grid grid-cols-2 gap-4 p-4 bg-white/80">
        {playerCreature.collections?.skills?.length > 0 ? (
          playerCreature.collections.skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              className="w-full h-full"
            />
          ))
        ) : (
          <div className="col-span-2 flex items-center justify-center text-gray-500">
            No skills available
          </div>
        )}
      </div>
    </div>
  )
}
