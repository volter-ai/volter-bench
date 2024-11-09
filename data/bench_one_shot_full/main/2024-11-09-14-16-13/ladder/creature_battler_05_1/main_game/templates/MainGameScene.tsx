import { useCurrentButtons } from "@/lib/useChoices.ts"
import { SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
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
    is_physical: boolean
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
    attack: number
    defense: number
    sp_attack: number
    sp_defense: number
    speed: number
  }
  meta: {
    prototype_id: string
    category: string
    creature_type: string
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
  meta: {
    prototype_id: string
    category: string
  }
  entities: {
    active_creature?: Creature
  }
  collections: {
    creatures: Creature[]
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
  const opponentCreature = props.data.entities.bot?.entities.active_creature

  if (!playerCreature || !opponentCreature) {
    return null
  }

  return (
    <div className="h-screen w-full flex flex-col bg-slate-900">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex justify-start items-start">
          <PlayerCard
            uid={props.data.entities.bot.uid}
            name={props.data.entities.bot.display_name}
            imageUrl={`/players/${props.data.entities.bot.meta.prototype_id}.png`}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
          />
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
          />
        </div>

        {/* Player Status */}
        <div className="flex justify-end items-end">
          <PlayerCard
            uid={props.data.entities.player.uid}
            name={props.data.entities.player.display_name}
            imageUrl={`/players/${props.data.entities.player.meta.prototype_id}.png`}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 bg-slate-800">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && playerCreature.collections.skills.map(skill => (
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

          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
              className="flex items-center gap-2"
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
