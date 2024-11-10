import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
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
    <div className="h-screen w-screen aspect-[16/9] flex flex-col">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {bot?.uid && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl={`/players/${bot.uid}.png`}
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          {botCreature?.uid && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              imageUrl={`/creatures/${botCreature.uid}.png`}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          {playerCreature?.uid && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.uid}.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {player?.uid && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/players/${player.uid}.png`}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 bg-slate-200">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && 
            playerCreature?.collections.skills.map((skill) => (
              skill?.uid && (
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
              )
            ))
          }
          
          {availableButtonSlugs.includes('back') && (
            <Button variant="outline" className="flex items-center gap-2">
              <ArrowLeft /> Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button variant="outline" className="flex items-center gap-2">
              <SwapHorizontal /> Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
