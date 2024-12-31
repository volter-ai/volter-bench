import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import withClickable from "@/lib/withClickable.tsx"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string;
  name: string;
  imageSrc: string;
  hp: number;
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ uid, name, imageSrc, hp, className, ...props }, ref) => (
    <Card ref={ref} className={className} {...props}>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <img src={imageSrc} alt={`${name} image`} className="w-full h-auto" />
        <p>HP: {hp}</p>
      </CardContent>
    </Card>
  )
)

CreatureCard.displayName = "CreatureCard"
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
