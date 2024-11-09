import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  slug: string
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
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
    player_creature: Creature | null
    bot_creature: Creature | null
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature

  // More robust skill filtering logic
  const availableSkills = playerCreature?.collections?.skills?.filter(
    skill => availableButtonSlugs.includes(skill?.slug)
  ) || []

  return (
    <div className="w-full h-full flex flex-col bg-background">
      {/* HUD */}
      <div className="h-16 bg-secondary flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          <span>Player: {props.data.entities.player?.display_name ?? 'Unknown'}</span>
        </div>
        <div className="flex items-center gap-2">
          <Swords className="h-5 w-5" />
          <span>VS</span>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          <span>Opponent: {props.data.entities.bot?.display_name ?? 'Unknown'}</span>
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between px-16 bg-secondary/10">
        <div className="flex flex-col items-center gap-2">
          <span className="text-sm font-bold">Your Creature</span>
          {playerCreature ? (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
            />
          ) : (
            <div className="w-[250px] h-[300px] flex items-center justify-center border-2 border-dashed rounded-lg">
              No Creature Selected
            </div>
          )}
        </div>

        <div className="flex flex-col items-center gap-2">
          <span className="text-sm font-bold">Opponent's Creature</span>
          {botCreature ? (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={`/assets/creatures/${botCreature.meta.prototype_id}.png`}
            />
          ) : (
            <div className="w-[250px] h-[300px] flex items-center justify-center border-2 border-dashed rounded-lg">
              No Creature Present
            </div>
          )}
        </div>
      </div>

      {/* Action UI */}
      <div className="h-[200px] bg-secondary/20 p-4 border-t">
        <div className="grid grid-cols-2 gap-4 h-full max-w-xl mx-auto">
          {availableSkills.length > 0 ? (
            availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                onClick={() => skill?.slug && emitButtonClick(skill.slug)}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center h-full text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
