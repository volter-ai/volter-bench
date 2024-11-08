import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap } from 'lucide-react';

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
            imageUrl={`/creatures/${opponentCreature.uid}/front.png`}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-start justify-end">
          <div className="relative">
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            <img 
              src={`/creatures/${opponentCreature.uid}/front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-end justify-start">
          <div className="relative">
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            <img
              src={`/creatures/${playerCreature.uid}/back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.uid}/back.png`}
          />
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 grid grid-cols-2 gap-4 p-4 bg-white">
        {playerCreature.collections.skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
            type={skill.meta.skill_type}
            className="w-full h-full"
          />
        ))}
      </div>
    </div>
  )
}
