import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { cn } from "@/lib/utils"

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

  if (!player_creature || !bot_creature || !player || !bot) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="h-screen w-full grid grid-rows-[auto_1fr_auto]">
      {/* HUD */}
      <nav className="bg-gray-800 p-4 text-white flex justify-between items-center">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="" // Left empty as per data structure
            className={cn("w-[200px] bg-blue-700")}
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl="" // Left empty as per data structure
            className={cn("w-[200px] bg-red-700")}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <main className="flex justify-between items-center px-8 bg-gradient-to-b from-blue-50 to-blue-100">
        <div className="relative">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl="" // Left empty as per data structure
            className={cn("transform hover:scale-105 transition-transform")}
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
            imageUrl="" // Left empty as per data structure
            className={cn("transform hover:scale-105 transition-transform")}
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </main>

      {/* UI Section */}
      <section className="bg-gray-100 p-4 rounded-t-lg">
        <div className="flex flex-wrap gap-2 justify-center">
          {player_creature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={skill.stats}
              className={cn("min-w-[120px]")}
            />
          ))}
          {(!player_creature.collections.skills || player_creature.collections.skills.length === 0) && (
            <div className="text-gray-500">No skills available</div>
          )}
        </div>
      </section>
    </div>
  )
}
