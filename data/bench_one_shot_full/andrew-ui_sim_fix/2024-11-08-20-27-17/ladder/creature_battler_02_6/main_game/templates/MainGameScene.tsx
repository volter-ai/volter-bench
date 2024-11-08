import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
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

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  if (!playerCreature || !botCreature || !player || !bot) {
    return null // Safely handle missing core data
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-[10%] w-full bg-muted/20 flex items-center justify-between px-4 border-b">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl={player.meta.image_url || '/images/default-player.png'}
        />
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl={bot.meta.image_url || '/images/default-player.png'}
        />
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center px-16">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={playerCreature.meta.image_url || '/images/default-creature.png'}
          />
          <div className="mt-2 text-sm font-semibold">Your Creature</div>
        </div>

        <div className="flex flex-col items-center">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={botCreature.meta.image_url || '/images/default-creature.png'}
          />
          <div className="mt-2 text-sm font-semibold">Opponent's Creature</div>
        </div>
      </div>

      {/* Skills/Controls Area */}
      <div className="h-[30%] bg-muted/10 p-4 border-t">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {playerCreature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={skill.stats}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
