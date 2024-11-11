import { useCurrentButtons } from "@/lib/useChoices"
import { Sword, RefreshCw, LogOut, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()
  const { player, bot } = props.data.entities

  return (
    <div className="relative h-screen w-screen aspect-[16/9] flex flex-col bg-slate-900">
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-6">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {bot?.entities?.active_creature && (
            <CreatureCard
              uid={bot.entities.active_creature.uid}
              name={bot.entities.active_creature.display_name}
              image="/placeholder/opponent.png"
              currentHp={bot.entities.active_creature.stats.hp}
              maxHp={bot.entities.active_creature.stats.max_hp}
              className="w-[250px] bg-slate-800/50"
            />
          )}
        </div>

        {/* Top Right - Opponent Player */}
        <div className="flex justify-end items-start">
          {bot && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl="/placeholder/opponent-avatar.png"
              className="w-[200px] bg-slate-800/50"
            />
          )}
        </div>

        {/* Bottom Left - Player Info */}
        <div className="flex justify-start items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder/player-avatar.png"
              className="w-[200px] bg-slate-800/50"
            />
          )}
        </div>

        {/* Bottom Right - Player Creature Status */}
        <div className="flex justify-end items-end">
          {player?.entities?.active_creature && (
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              image="/placeholder/player.png"
              currentHp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
              className="w-[250px] bg-slate-800/50"
            />
          )}
        </div>
      </div>

      <div className="h-1/3 p-6 bg-slate-800">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && 
            player?.entities?.active_creature?.collections?.skills?.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage,
                  type: skill.meta.skill_type
                }}
                className="w-full h-full text-lg"
                variant="secondary"
              />
            ))}
          
          {availableButtonSlugs.includes('swap') && (
            <Button 
              onClick={() => emitButtonClick('swap')}
              className="w-full h-full text-lg"
              variant="secondary"
            >
              <SwapHorizontal className="mr-2 h-5 w-5" />
              Swap
            </Button>
          )}
          
          {availableButtonSlugs.includes('play-again') && (
            <Button
              onClick={() => emitButtonClick('play-again')}
              className="w-full h-full text-lg"
              variant="secondary"
            >
              <RefreshCw className="mr-2 h-5 w-5" />
              Play Again
            </Button>
          )}
          
          {availableButtonSlugs.includes('quit') && (
            <Button
              onClick={() => emitButtonClick('quit')}
              className="w-full h-full text-lg"
              variant="destructive"
            >
              <LogOut className="mr-2 h-5 w-5" />
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
