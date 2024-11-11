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
  meta: {
    image_url?: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  description: string
  collections: {
    creatures: Creature[]
  }
  meta: {
    image_url?: string
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
    <div className="h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <div className="h-16 border-b flex items-center justify-between px-4">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={player.meta.image_url || '/default_player.png'}
          />
        )}
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span className="font-bold">Battle Arena</span>
          <Swords className="h-6 w-6" />
        </div>
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={bot.meta.image_url || '/default_player.png'}
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-16">
        {player_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full">
              Player
            </div>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={player_creature.meta.image_url || '/default_creature.png'}
            />
          </div>
        )}

        {bot_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full">
              Opponent
            </div>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={bot_creature.meta.image_url || '/default_creature.png'}
            />
          </div>
        )}
      </div>

      {/* UI Region */}
      <div className="h-1/3 border-t bg-muted p-4">
        <div className="grid grid-cols-4 gap-4">
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
      </div>
    </div>
  )
}
