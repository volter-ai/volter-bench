import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Play, X } from 'lucide-react';

interface ExamplePlayer {
    uid: string,
    stats: {
        stat1: number,
    },
}

interface GameUIData {
    entities: {
        player: ExamplePlayer
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    // Log availableButtonSlugs to ensure they are populated
    console.log("Available Button Slugs:", availableButtonSlugs);

    const getButtonIcon = (slug: string) => {
        switch (slug) {
            case 'play':
                return <Play className="mr-2 h-4 w-4" />;
            case 'quit':
                return <X className="mr-2 h-4 w-4" />;
            default:
                return null;
        }
    };

    const getButtonText = (slug: string) => {
        return slug.charAt(0).toUpperCase() + slug.slice(1);
    };

    return (
        <div className="min-h-screen flex flex-col justify-between items-center p-8 bg-gray-800 text-white">
            <div className="text-4xl font-bold mt-16">
                Game Title
            </div>
            
            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.map((slug) => (
                    <Button
                        key={slug}
                        onClick={() => {
                            console.log(`Button clicked: ${slug}`);
                            emitButtonClick(slug);
                        }}
                        className="w-48"
                    >
                        {getButtonIcon(slug)}
                        {getButtonText(slug)}
                    </Button>
                ))}
            </div>
        </div>
    );
}
