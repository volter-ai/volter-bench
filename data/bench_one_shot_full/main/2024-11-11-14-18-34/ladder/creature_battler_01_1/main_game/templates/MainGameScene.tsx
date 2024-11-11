import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
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
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const player = props.data?.entities?.player
  const bot = props.data?.entities?.bot
  const playerCreature = props.data?.entities?.player_creature
  const botCreature = props.data?.entities?.bot_creature

  if (!player || !bot) {
    return <div className="h-full w-full flex items-center justify-center">
      Loading players...
    </div>
  }

  return (
    <div className="h-full w-full aspect-video relative flex flex-col">
      {/* HUD */}
      <div className="w-full h-[15%] bg-slate-800 flex items-center justify-between px-6">
        <PlayerCard
          uid={player.uid}
          name={player?.display_name ?? 'Player'}
          imageUrl="/placeholder-player.png"
        />
        <PlayerCard
          uid={bot.uid}
          name={bot?.display_name ?? 'Opponent'}
          imageUrl="/placeholder-opponent.png"
        />
      </div>

      {/* Battlefield */}
      <div className="h-[50%] flex justify-between items-center px-12">
        {playerCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-0 flex items-center gap-2">
              <Shield className="w-5 h-5" />
              <span className="text-sm font-bold">Your Creature</span>
            </div>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature?.display_name ?? 'Unknown Creature'}
              hp={playerCreature?.stats?.hp ?? 0}
              maxHp={playerCreature?.stats?.max_hp ?? 0}
              imageUrl="/placeholder-creature.png"
            />
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <div className="absolute -top-8 right-0 flex items-center gap-2">
              <Sword className="w-5 h-5" />
              <span className="text-sm font-bold">Opponent's Creature</span>
            </div>
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature?.display_name ?? 'Unknown Creature'}
              hp={botCreature?.stats?.hp ?? 0}
              maxHp={botCreature?.stats?.max_hp ?? 0}
              imageUrl="/placeholder-creature.png"
            />
          </div>
        )}
      </div>

      {/* UI Area */}
      <div className="h-[35%] bg-slate-700 p-4 flex flex-col gap-4">
        <div className="grid grid-cols-4 gap-4">
          {playerCreature?.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill?.display_name ?? 'Unknown Skill'}
              description={skill?.description ?? 'No description available'}
              stats={`Damage: ${skill?.stats?.damage ?? 0}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
