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
  }
  meta: {
    image_url?: string
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
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature, player, opponent } = props.data.entities

  // Default images if none provided in meta
  const defaultPlayerImage = "/assets/default-player.png"
  const defaultCreatureImage = "/assets/default-creature.png"

  if (!player_creature || !opponent_creature || !player || !opponent) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="h-screen w-full grid grid-rows-[auto_1fr_auto] bg-background">
      {/* HUD */}
      <nav className="w-full p-4 bg-muted/20">
        <div className="flex justify-between items-center">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={player.meta.image_url || defaultPlayerImage}
          />
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={opponent.meta.image_url || defaultPlayerImage}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <main className="flex justify-between items-center p-8 bg-muted/10">
        <div className="flex flex-col items-center gap-4">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={player_creature.meta.image_url || defaultCreatureImage}
          />
          <div className="flex gap-2">
            <div className="flex items-center gap-1">
              <Sword className="w-4 h-4" />
              <span>{player_creature.stats.attack}</span>
            </div>
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              <span>{player_creature.stats.defense}</span>
            </div>
            <div className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              <span>{player_creature.stats.speed}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-center gap-4">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl={opponent_creature.meta.image_url || defaultCreatureImage}
          />
          <div className="flex gap-2">
            <div className="flex items-center gap-1">
              <Sword className="w-4 h-4" />
              <span>{opponent_creature.stats.attack}</span>
            </div>
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              <span>{opponent_creature.stats.defense}</span>
            </div>
            <div className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              <span>{opponent_creature.stats.speed}</span>
            </div>
          </div>
        </div>
      </main>

      {/* Skills UI */}
      <footer className="p-4 bg-muted/20">
        <div className="flex flex-wrap gap-2 justify-center">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
            />
          ))}
        </div>
      </footer>
    </div>
  )
}
