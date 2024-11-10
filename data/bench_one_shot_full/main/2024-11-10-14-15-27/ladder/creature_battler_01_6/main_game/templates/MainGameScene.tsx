import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
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

  const { player, bot, player_creature, bot_creature } = props.data.entities

  return (
    <div className="h-screen w-full flex flex-col">
      <nav className="h-16 bg-primary/10 flex items-center justify-between px-4">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/player.png`}
          />
        )}
        <div className="flex items-center gap-4">
          <Shield className="h-6 w-6" />
          <span>Battle Arena</span>
          <Swords className="h-6 w-6" />
        </div>
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/bot.png`}
          />
        )}
      </nav>

      <main className="flex-grow flex items-center justify-between px-8">
        {player_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Your Creature
            </span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}

        {bot_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Opponent's Creature
            </span>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={`/creatures/${bot_creature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}
      </main>

      <section className="h-1/3 bg-secondary/10 p-4 flex flex-col gap-4">
        <div className="grid grid-cols-3 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </section>
    </div>
  )
}
