import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
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
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface GameUIData {
  entities: {
    player_creature: Creature
    foe_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const foeCreature = props.data?.entities?.foe_creature

  if (!playerCreature || !foeCreature) {
    return <div className="text-center p-4">Loading battle...</div>
  }

  return (
    <div className="h-screen aspect-video bg-background grid grid-rows-[auto_1fr_auto]">
      {/* Top HUD */}
      <nav className="bg-muted p-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Sword className="w-4 h-4" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4" />
          <span>Round 1</span>
        </div>
      </nav>

      {/* Battlefield */}
      <main className="p-8 flex justify-between items-center">
        <div className="relative">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats?.hp ?? 0}
            maxHp={playerCreature.stats?.max_hp ?? 0}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
            className="relative"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
            Player
          </div>
        </div>

        <div className="relative">
          <CreatureCard
            uid={foeCreature.uid}
            name={foeCreature.display_name}
            hp={foeCreature.stats?.hp ?? 0}
            maxHp={foeCreature.stats?.max_hp ?? 0}
            imageUrl={`/creatures/${foeCreature.meta.prototype_id}.png`}
            className="relative"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </main>

      {/* Skills UI */}
      <footer className="bg-muted/50 p-4">
        <div className="grid grid-cols-4 gap-4 max-w-2xl mx-auto">
          {playerCreature.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description ?? ''}
              stats={`Damage: ${skill.stats?.damage ?? 0}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </footer>
    </div>
  )
}
