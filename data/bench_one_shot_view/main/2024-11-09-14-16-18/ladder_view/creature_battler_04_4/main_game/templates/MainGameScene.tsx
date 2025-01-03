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
  meta: {
    creature_type: string
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
  uid: string
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
    return <div uid={`${props.data.uid}-loading`} className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div uid={props.data.uid} className="h-screen w-screen aspect-[16/9] flex flex-col bg-gradient-to-b from-sky-100 to-sky-300">
      {/* Battlefield Area (upper 2/3) */}
      <div uid={`${props.data.uid}-battlefield`} className="flex-grow grid grid-cols-2 gap-4 p-6">
        {/* Top Left - Opponent Status */}
        <div uid={`${props.data.uid}-opponent-status`} className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.creature_type}_front.png`}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div uid={`${props.data.uid}-opponent-creature`} className="flex justify-end items-start">
          <div uid={`${props.data.uid}-opponent-creature-container`} className="relative">
            <div uid={`${props.data.uid}-opponent-shadow`} className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <CreatureCard
              uid={`${opponentCreature.uid}-battle`}
              name={opponentCreature.display_name}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              imageUrl={`/creatures/${opponentCreature.meta.creature_type}_front.png`}
            />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div uid={`${props.data.uid}-player-creature`} className="flex justify-start items-end">
          <div uid={`${props.data.uid}-player-creature-container`} className="relative">
            <div uid={`${props.data.uid}-player-shadow`} className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <CreatureCard
              uid={`${playerCreature.uid}-battle`}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.meta.creature_type}_back.png`}
            />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div uid={`${props.data.uid}-player-status`} className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.creature_type}_back.png`}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div uid={`${props.data.uid}-ui-area`} className="h-1/3 grid grid-cols-2 gap-4 p-6 bg-white/80">
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
  )
}
