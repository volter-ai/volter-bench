import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
    prototype_id: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
  meta: {
    prototype_id: string
  }
}

interface GameUIData {
  entities: {
    player: Player
    foe: Player
    player_creature: Creature
    foe_creature: Creature
  }
  collections: {
    player_skill_queue: any[]
    foe_skill_queue: any[]
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const foeCreature = props.data.entities.foe_creature
  const player = props.data.entities.player
  const foe = props.data.entities.foe

  // Generate image URLs based on prototype IDs
  const getImageUrl = (entity: { meta: { prototype_id: string }}) => 
    `/assets/sprites/${entity.meta.prototype_id}.png`

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <div className="h-16 bg-secondary flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-4">
          <Sword className="h-6 w-6" />
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={getImageUrl(player)}
            />
          )}
        </div>
        <div className="flex items-center gap-4">
          {foe && (
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl={getImageUrl(foe)}
            />
          )}
          <Shield className="h-6 w-6" />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8 bg-background/50">
        {playerCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
              Your Creature
            </div>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={getImageUrl(playerCreature)}
            />
          </div>
        )}

        {foeCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
              Opponent's Creature
            </div>
            <CreatureCard
              uid={foeCreature.uid}
              name={foeCreature.display_name}
              hp={foeCreature.stats.hp}
              maxHp={foeCreature.stats.max_hp}
              imageUrl={getImageUrl(foeCreature)}
            />
          </div>
        )}
      </div>

      {/* Skills/UI Area */}
      <div className="h-1/3 bg-secondary/50 p-4 border-t">
        <div className="grid grid-cols-3 gap-4 h-full">
          {playerCreature?.collections.skills.map((skill) => (
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
