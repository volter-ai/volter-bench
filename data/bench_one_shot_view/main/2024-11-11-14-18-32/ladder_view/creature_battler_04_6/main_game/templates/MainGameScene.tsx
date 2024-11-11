import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.creature_type}/front.png`}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-start justify-end">
          {/* Platform/shadow would go here */}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-end justify-start">
          {/* Platform/shadow would go here */}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.creature_type}/back.png`}
          />
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 p-4 bg-white">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {playerCreature.collections.skills.map((skill) => (
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
