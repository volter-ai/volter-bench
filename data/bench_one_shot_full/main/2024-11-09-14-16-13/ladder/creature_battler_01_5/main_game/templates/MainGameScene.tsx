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
  meta: {
    prototype_id: string
    category: string
  }
  entities: Record<string, never>
  collections: Record<string, never>
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
    prototype_id: string
    category: string
  }
  entities: Record<string, never>
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  description: string
  stats: Record<string, never>
  meta: {
    prototype_id: string
    category: string
  }
  entities: Record<string, never>
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
    return <div className="h-screen w-full flex items-center justify-center">
      Loading game state...
    </div>
  }

  const handleSkillClick = (skill: Skill) => {
    if (!skill?.meta?.prototype_id) return
    const slug = skill.meta.prototype_id
    if (availableButtonSlugs.includes(slug)) {
      emitButtonClick(slug)
    }
  }

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      <nav className="h-14 bg-primary/10 flex items-center justify-between px-4">
        {player.__type === "Player" && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta.prototype_id}.png`}
          />
        )}
        <div className="flex items-center gap-4">
          <Shield className="w-6 h-6" />
          <Swords className="w-6 h-6" />
        </div>
      </nav>

      <main className="flex-grow flex items-center justify-between px-12 py-4">
        {player_creature.__type === "Creature" && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
            />
          </div>
        )}

        {bot_creature.__type === "Creature" && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold">Opponent's Creature</span>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={`/creatures/${bot_creature.meta.prototype_id}.png`}
            />
          </div>
        )}
      </main>

      <div className="h-2/5 bg-secondary/10 p-6">
        <div className="flex flex-wrap gap-4 h-full overflow-y-auto">
          {player_creature.collections.skills
            .filter(skill => skill.__type === "Skill" && skill.meta?.prototype_id)
            .map((skill) => (
              <div key={skill.uid} className="w-full sm:w-[calc(50%-1rem)] md:w-[calc(33.33%-1rem)]">
                <SkillButton
                  uid={skill.uid}
                  name={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  disabled={!availableButtonSlugs.includes(skill.meta.prototype_id)}
                  onClick={() => handleSkillClick(skill)}
                />
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
