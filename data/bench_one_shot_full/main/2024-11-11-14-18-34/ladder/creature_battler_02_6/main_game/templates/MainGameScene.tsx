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
  meta: {
    image_url?: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    image_url?: string
  }
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
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading game...
    </div>
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="w-full p-4 border-b flex justify-between items-center">
        {player && (
          <PlayerCard 
            uid={player.uid}
            name={player.display_name}
            imageUrl={player.meta.image_url || "/default/player.png"}
          />
        )}
        <div className="flex gap-4">
          <Shield className="w-6 h-6" />
          <Swords className="w-6 h-6" />
        </div>
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={bot.meta.image_url || "/default/opponent.png"}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-8">
        {player_creature && (
          <div className="flex flex-col items-center gap-4">
            <span className="text-lg font-bold">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={player_creature.meta.image_url || "/default/creature.png"}
            />
          </div>
        )}

        {bot_creature && (
          <div className="flex flex-col items-center gap-4">
            <span className="text-lg font-bold">Opponent's Creature</span>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              currentHp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={bot_creature.meta.image_url || "/default/creature.png"}
            />
          </div>
        )}
      </div>

      {/* UI Region */}
      <div className="h-48 border-t p-4 bg-muted">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections?.skills?.map((skill) => (
            skill && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              />
            )
          ))}
        </div>
      </div>
    </div>
  )
}
