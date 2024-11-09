import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, RefreshCw, LogOut, SwapHorizontal } from 'lucide-react'
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()
  const { player, bot } = props.data.entities

  const renderActionButtons = () => {
    const buttons = []
    
    if (availableButtonSlugs.includes('attack') && player?.entities?.active_creature) {
      const skills = player.entities.active_creature.collections.skills
      skills.slice(0, 4).forEach(skill => {
        buttons.push(
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            name={skill.display_name}
            description={skill.description}
            stats={{
              damage: skill.stats.base_damage
            }}
            onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
          />
        )
      })
    }

    if (availableButtonSlugs.includes('swap')) {
      buttons.push(
        <Button
          key="swap"
          uid="swap-button"
          onClick={() => emitButtonClick('swap')}
          className="flex items-center gap-2"
        >
          <SwapHorizontal className="w-4 h-4" />
          Swap
        </Button>
      )
    }

    if (availableButtonSlugs.includes('play-again')) {
      buttons.push(
        <Button
          key="play-again"
          uid="play-again-button"
          onClick={() => emitButtonClick('play-again')}
          className="flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Play Again
        </Button>
      )
    }

    if (availableButtonSlugs.includes('quit')) {
      buttons.push(
        <Button
          key="quit"
          uid="quit-button"
          onClick={() => emitButtonClick('quit')}
          className="flex items-center gap-2"
        >
          <LogOut className="w-4 h-4" />
          Quit
        </Button>
      )
    }

    // Ensure we always have a 2x2 grid by padding with empty divs
    while (buttons.length < 4) {
      buttons.push(<div key={`empty-${buttons.length}`} />)
    }

    return buttons
  }

  return (
    <div className="w-full h-full aspect-[16/9] flex flex-col">
      {/* Battlefield Area (2/3) */}
      <div className="flex-[2] grid grid-cols-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {bot?.entities?.active_creature && (
            <CreatureCard
              uid={bot.entities.active_creature.uid}
              name={bot.entities.active_creature.display_name}
              hp={bot.entities.active_creature.stats.hp}
              maxHp={bot.entities.active_creature.stats.max_hp}
              imageUrl="/placeholder.png"
            />
          )}
        </div>

        {/* Top Right - Opponent Info */}
        <div className="flex justify-end items-start">
          {bot && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl="/placeholder.png"
            />
          )}
        </div>

        {/* Bottom Left - Player Info */}
        <div className="flex justify-start items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder.png"
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {player?.entities?.active_creature && (
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              hp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
              imageUrl="/placeholder.png"
            />
          )}
        </div>
      </div>

      {/* UI Area (1/3) */}
      <div className="flex-1 p-4 bg-white">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {renderActionButtons()}
        </div>
      </div>
    </div>
  )
}
