import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
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
    [key: string]: any
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
    speed: number
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

  const { player, bot, player_creature, bot_creature } = props.data.entities

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="text-center p-4">Loading battle...</div>
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-900">
      {/* HUD */}
      <nav className="h-24 bg-slate-800 flex items-center justify-between px-4">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl="" // Placeholder - should be provided by backend
        />
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl="" // Placeholder - should be provided by backend
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8">
        <div className="relative">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl="" // Placeholder - should be provided by backend
            className="transform scale-x-1"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
            Player
          </div>
        </div>

        <div className="relative">
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            currentHp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl="" // Placeholder - should be provided by backend
            className="transform scale-x-[-1]"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </div>

      {/* Action UI */}
      <div className="h-1/4 bg-slate-800 rounded-t-lg p-4">
        <div className="flex flex-wrap gap-2 justify-center">
          {player_creature.collections?.skills?.length > 0 ? (
            player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              />
            ))
          ) : (
            <div className="text-center text-slate-400">No skills available</div>
          )}
        </div>
      </div>
    </div>
  )
}
