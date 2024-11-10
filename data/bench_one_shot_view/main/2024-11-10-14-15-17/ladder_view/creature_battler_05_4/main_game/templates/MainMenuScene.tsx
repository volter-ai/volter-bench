import { useCurrentButtons } from "@/lib/useChoices";
import { Play, Power } from 'lucide-react'

interface Stats {
    [key: string]: number
}

interface Meta {
    prototype_id: string
    category: string
    [key: string]: string
}

interface BaseEntity {
    __type: string
    uid: string
    display_name: string
    description: string
    stats: Stats
    meta: Meta
    entities: Record<string, any>
    collections: Record<string, any[]>
}

interface Skill extends BaseEntity {
    __type: 'Skill'
    stats: {
        base_damage: number
    }
    meta: {
        skill_type: string
        is_physical: boolean
    } & Meta
}

interface Creature extends BaseEntity {
    __type: 'Creature'
    stats: {
        hp: number
        max_hp: number
        attack: number
        defense: number
        sp_attack: number
        sp_defense: number
        speed: number
    }
    meta: {
        creature_type: string
    } & Meta
    collections: {
        skills: Skill[]
    }
}

interface Player extends BaseEntity {
    __type: 'Player'
    entities: {
        active_creature?: Creature
    }
    collections: {
        creatures: Creature[]
    }
}

interface GameUIData {
    entities: {
        player: Player
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-blue-900 to-blue-950">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        CREATURE BATTLE
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-64">
                    {availableButtonSlugs.includes('play') && (
                        <button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center gap-2 w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                        >
                            <Play size={24} />
                            <span className="text-xl">Play Game</span>
                        </button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center gap-2 w-full px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                        >
                            <Power size={24} />
                            <span className="text-xl">Quit</span>
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
