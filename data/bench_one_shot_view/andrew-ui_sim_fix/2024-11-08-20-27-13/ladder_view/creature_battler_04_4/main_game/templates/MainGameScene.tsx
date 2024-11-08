import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage?: number
  }
  meta: {
    skill_type?: string
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
  meta: {
    creature_type: string
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

  // Temporary image URLs since they're not in the data
  const getCreatureImageUrl = (creature: Creature) => 
    `/images/creatures/${creature.meta.creature_type}/${creature.uid}.png`

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-800">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(opponentCreature)}
              className="transform scale-75 origin-top-left"
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            {/* Platform/Shadow Effect */}
            <div className="absolute bottom-0 w-32 h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            {/* Platform/Shadow Effect */}
            <div className="absolute bottom-0 w-32 h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(playerCreature)}
              className="transform scale-75 origin-bottom-right"
            />
          )}
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 p-4 bg-slate-900">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              className="w-full h-full text-lg"
            />
          ))}
        </div>
      </div>
    </div>
  )
}
