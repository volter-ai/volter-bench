import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  stats: {
    damage: number
  }
  uid: string
  display_name: string
  description: string
}

interface Creature {
  __type: "Creature"
  stats: {
    hp: number
    max_hp: number
  }
  uid: string
  display_name: string
  description: string
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

  const { player, bot, player_creature, bot_creature } = props.data?.entities || {}

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="w-full h-screen flex flex-col">
      {/* HUD */}
      <nav className="w-full h-16 bg-slate-800 flex items-center justify-between px-4">
        <div className="flex items-center gap-4 text-white">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/player-avatar.png"
          />
          <div className="flex items-center gap-2">
            <Sword className="h-5 w-5" />
            <span>Battle Scene</span>
          </div>
        </div>
        <div className="flex items-center gap-4 text-white">
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            <span>Turn 1</span>
          </div>
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl="/bot-avatar.png"
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8 bg-slate-200">
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Your Creature
          </span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl="/creature-placeholder.png"
          />
        </div>

        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Opponent's Creature
          </span>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl="/creature-placeholder.png"
          />
        </div>
      </div>

      {/* UI Region */}
      <div className="h-1/3 bg-slate-100 p-4 flex flex-col gap-4">
        {player_creature.collections?.skills?.length > 0 ? (
          <div className="grid grid-cols-3 gap-4">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-slate-500">
            No skills available
          </div>
        )}
      </div>
    </div>
  )
}
