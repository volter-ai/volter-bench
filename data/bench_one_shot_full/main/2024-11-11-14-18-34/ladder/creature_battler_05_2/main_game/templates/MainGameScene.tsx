import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-800" uid="main-game-container">
      {/* Battlefield Area */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4" uid="battlefield-container">
        {/* Top Left - Bot Status */}
        <div className="flex justify-start items-start" uid="bot-status-container">
          {bot && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl="/players/bot.png"
            />
          )}
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl="/creatures/default.png"
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex justify-end items-start" uid="bot-creature-container">
          {botCreature && (
            <CreatureCard
              uid={`${botCreature.uid}-display`}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl="/creatures/default.png"
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end" uid="player-creature-container">
          {playerCreature && (
            <CreatureCard
              uid={`${playerCreature.uid}-display`}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl="/creatures/default.png"
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end" uid="player-status-container">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/players/player.png"
            />
          )}
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl="/creatures/default.png"
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-900 p-4" uid="ui-container">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full" uid="button-grid">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill, index) => (
            <div key={skill.uid} uid={`skill-container-${index}`} className="flex justify-center items-center">
              <SkillButton
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                type={skill.meta.skill_type}
              />
            </div>
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <div uid="back-button-container" className="flex justify-center items-center">
              <SkillButton
                uid="back-button"
                name="Back"
                description="Return to previous screen"
              />
            </div>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <div uid="swap-button-container" className="flex justify-center items-center">
              <SkillButton
                uid="swap-button"
                name="Swap Creature"
                description="Switch to a different creature"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
