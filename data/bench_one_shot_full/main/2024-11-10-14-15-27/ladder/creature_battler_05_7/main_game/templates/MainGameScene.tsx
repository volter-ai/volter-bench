import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Swords, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
  description: string
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const botCreature = props.data.entities.bot?.entities.active_creature

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex items-center justify-center">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl="" // Placeholder - actual image URL should come from data
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {props.data.entities.bot && (
            <PlayerCard
              uid={props.data.entities.bot.uid}
              name={props.data.entities.bot.display_name}
              imageUrl="" // Placeholder - actual image URL should come from data
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {props.data.entities.player && (
            <PlayerCard
              uid={props.data.entities.player.uid}
              name={props.data.entities.player.display_name}
              imageUrl="" // Placeholder - actual image URL should come from data
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl="" // Placeholder - actual image URL should come from data
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-white">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
            />
          ))}
          {availableButtonSlugs.includes('swap') && props.data.entities.player && (
            <Button 
              className="w-full h-full flex items-center justify-center gap-2"
              onClick={() => emitButtonClick('swap')}
            >
              <SwapHorizontal className="w-4 h-4" />
              Swap Creature
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
