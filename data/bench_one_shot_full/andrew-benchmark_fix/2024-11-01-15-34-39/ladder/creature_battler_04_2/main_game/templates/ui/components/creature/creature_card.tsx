import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"

interface CreatureCardProps extends React.ComponentPropsWithoutRef<typeof ShadcnCard> {
  uid: string;
  name: string;
  image: string;
  hp: number;
  maxHp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, hp, maxHp, ...props }, ref) => (
    <ShadcnCard ref={ref} className={cn("w-64", className)} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center">
        <img src={image} alt={name} className="w-32 h-32 object-contain mb-4" />
        <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
          <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${(hp / maxHp) * 100}%` }}></div>
        </div>
        <p className="mt-2">{`HP: ${hp}/${maxHp}`}</p>
      </CardContent>
    </ShadcnCard>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
