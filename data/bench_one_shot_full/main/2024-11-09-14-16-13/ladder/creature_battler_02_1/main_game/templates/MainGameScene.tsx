import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
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
  meta: {
    prototype_id: string
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
    prototype_id: string
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

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  // Generate image URLs based on prototype IDs
  const getImageUrl = (type: string, id: string) => `/assets/${type}/${id}.png`

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* Top HUD */}
      <nav className="w-full h-16 bg-primary/10 flex items-center justify-between px-6">
        {player && (
          <PlayerCard 
            uid={player.uid}
            name={player.display_name}
            imageUrl={getImageUrl('players', player.meta.prototype_id)}
          />
        )}
        {bot && (
          <PlayerCard 
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={getImageUrl('players', bot.meta.prototype_id)}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center px-20">
        {playerCreature && (
          <div className="relative">
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={getImageUrl('creatures', playerCreature.meta.prototype_id)}
            />
            <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
              Player
            </div>
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={getImageUrl('creatures', botCreature.meta.prototype_id)}
            />
            <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
              Opponent
            </div>
          </div>
        )}
      </div>

      {/* Bottom UI */}
      <div className="h-48 bg-secondary/10 p-4">
        <div className="grid grid-cols-4 gap-4">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={skill.stats}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
