import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  slug: string
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

  const playerCreature = props.data.entities?.player_creature
  const botCreature = props.data.entities?.bot_creature
  const player = props.data.entities?.player
  const bot = props.data.entities?.bot

  if (!playerCreature || !botCreature || !player || !bot) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading game state...
    </div>
  }

  const handleSkillClick = (skill: Skill) => {
    if (availableButtonSlugs.includes(skill.slug)) {
      emitButtonClick(skill.slug)
    }
  }

  const skills = playerCreature.collections.skills || []

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <div className="h-[10%] border-b flex items-center justify-between px-6">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl="/default-player.png"
          className="w-[200px] h-[80px]"
        />
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl="/default-opponent.png"
          className="w-[200px] h-[80px]"
        />
      </div>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center px-20">
        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
            Player
          </div>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl="/default-creature.png"
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl="/default-creature.png"
          />
        </div>
      </div>

      {/* Controls */}
      <div className="h-[30%] border-t bg-muted/50 p-6">
        <div className="flex flex-wrap gap-4 justify-center">
          {skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
              disabled={!availableButtonSlugs.includes(skill.slug)}
              onClick={() => handleSkillClick(skill)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
