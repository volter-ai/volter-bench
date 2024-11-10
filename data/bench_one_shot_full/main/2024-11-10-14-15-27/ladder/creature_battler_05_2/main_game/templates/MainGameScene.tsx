import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { Button } from "@/components/ui/button"
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
    <div className="relative h-screen w-screen aspect-[16/9] bg-slate-900 flex flex-col">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-gradient-to-b from-slate-800 to-slate-900">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {bot && botCreature && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl="/players/opponent_avatar.png"
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          {botCreature && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <CreatureCard
                uid={botCreature.uid}
                name={botCreature.display_name}
                hp={botCreature.stats.hp}
                maxHp={botCreature.stats.max_hp}
                imageUrl={`/assets/creatures/${botCreature.uid}.png`}
              />
            </div>
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          {playerCreature && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
                imageUrl={`/assets/creatures/${playerCreature.uid}.png`}
              />
            </div>
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {player && playerCreature && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/players/player_avatar.png"
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-800/90 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
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
              onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button
              onClick={() => emitButtonClick('back')}
              className="flex items-center justify-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
              className="flex items-center justify-center gap-2"
            >
              <SwapHorizontal className="w-4 h-4" /> Swap Creature
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
