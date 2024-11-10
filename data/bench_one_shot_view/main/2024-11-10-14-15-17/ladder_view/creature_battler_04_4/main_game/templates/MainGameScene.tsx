import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Swords } from 'lucide-react';

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
    creature_type: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
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

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  // Placeholder image URLs since they're not in the data
  const getCreatureImageUrl = (creature: Creature) => 
    `/images/creatures/${creature.meta.creature_type}/${creature.meta.prototype_id}.png`

  return (
    <div className="h-screen w-screen flex flex-col bg-gradient-to-b from-sky-200 to-sky-300">
      {/* Battlefield - Upper 2/3 */}
      <div className="flex-grow-2 grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponentCreature && (
            <div className="flex items-center gap-2">
              <Shield className="w-6 h-6" />
              <div className="text-lg font-bold">{opponentCreature.display_name}</div>
            </div>
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(opponentCreature)}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(playerCreature)}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          {playerCreature && (
            <div className="flex items-center gap-2">
              <div className="text-lg font-bold">{playerCreature.display_name}</div>
              <Swords className="w-6 h-6" />
            </div>
          )}
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="flex-grow-1 bg-white/50 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {playerCreature?.collections.skills.map((skill) => (
            skill.__type === "Skill" && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                type={skill.meta.skill_type}
              />
            )
          ))}
        </div>
      </div>
    </div>
  )
}
