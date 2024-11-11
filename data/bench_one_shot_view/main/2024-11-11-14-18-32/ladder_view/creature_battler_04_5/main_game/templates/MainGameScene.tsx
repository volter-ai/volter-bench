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
    return null
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-800">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="flex-grow-2 relative grid grid-cols-2 p-4 gap-4">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/creatures/${opponentCreature.meta.creature_type}/front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img 
              src={`/creatures/${opponentCreature.meta.creature_type}/front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img
              src={`/creatures/${playerCreature.meta.creature_type}/back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/creatures/${playerCreature.meta.creature_type}/back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="flex-grow-1 grid grid-cols-2 gap-4 p-4 bg-slate-900">
        {playerCreature.collections.skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
            type={skill.meta.skill_type}
            disabled={!availableButtonSlugs.includes(skill.uid)}
            variant="secondary"
            className="w-full h-24"
          />
        ))}
      </div>
    </div>
  )
}
